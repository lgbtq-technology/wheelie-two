import logging

import requests
from flask import current_app

from app.services.slack_client import get_slack_client

logger = logging.getLogger(__name__)

CALLBACK_ID = "invite"


def send_signup_prompt(channel, user_data):
    """
    Send signup approval message to admin channel.
    """
    client = get_slack_client(current_app.config["SLACK_BOT_TOKEN"])

    message = {
        "channel": channel,
        "text": "New Signup!",
        "attachments": [
            {
                "title": user_data.get("email"),
                "fields": [
                    {
                        "title": "Social/Homepage",
                        "value": user_data.get("homepage", ""),
                        "short": True,
                    },
                    {
                        "title": "GitHub",
                        "value": user_data.get("github", ""),
                        "short": True,
                    },
                ],
                "author_name": user_data.get("name"),
                "author_icon": "https://api.slack.com/img/api/homepage_custom_integrations-2x.png",
            },
            {"title": "About Me", "text": user_data.get("about", "")},
            {
                "title": "Would you like to invite this person?",
                "callback_id": CALLBACK_ID,
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "invite",
                        "text": "Invite",
                        "type": "button",
                        "value": user_data.get("email"),
                    },
                    {"name": "no", "text": "No", "type": "button", "value": ""},
                ],
            },
        ],
    }

    client.chat_postMessage(**message)


def handle_invite(payload):
    """
    Handle invite button press.
    """
    token = current_app.config.get("SLACK_INVITE_TOKEN")
    if not token:
        app_url = current_app.config["APP_URL"]
        team_id = current_app.config["SLACK_TEAM_ID"]
        return {
            "token": current_app.config["SLACK_ACCESS_TOKEN"],
            "replace_original": False,
            "text": f":warning: No invite token configured. :warning: <{app_url}/install-inviter?team={team_id}|Authenticate the inviter>",
        }

    action = payload.get("actions", [{}])[0]
    email = action.get("value")

    if not email:
        # Rejection
        return update_invite_message(
            token,
            payload,
            {
                "title": "Signup Rejected",
                "color": "#CD2626",
                "text": f":no_good::skin-tone-5: Rejected by <@{payload['user']['id']}>",
            },
        )

    # Attempt invite
    domain = current_app.config["SLACK_TEAM_DOMAIN"]
    result = send_slack_invite(token, domain, email)

    user_id = payload["user"]["id"]

    if not result.get("ok"):
        error = result.get("error", "")
        if error in (
            "already_invited",
            "already_in_team",
            "already_in_team_invited_user",
        ):
            return update_invite_message(
                token,
                payload,
                {
                    "title": "Already Invited",
                    "color": "#FFFF00",
                    "text": f":information_desk_person::skin-tone-5: This person has already been invited! I can't resend invites, but you can <https://{domain}.slack.com/admin/invites|do it manually>.",
                },
            )
        elif error == "user_disabled":
            return update_invite_message(
                token,
                payload,
                {
                    "title": "Disabled Account",
                    "color": "#CD2626",
                    "text": ":thinking_face: User account was previously disabled.",
                },
            )
        else:
            return update_invite_message(
                token,
                payload,
                {
                    "title": "Error while inviting",
                    "color": "#CD2626",
                    "text": f":astonished: Received unknown `{error}` error while attempting to invite.",
                },
            )

    return update_invite_message(
        token,
        payload,
        {
            "title": "Invite Sent!",
            "color": "#AADD00",
            "text": f":ok_woman::skin-tone-5: Invited by <@{user_id}> :dancers: :tada:",
        },
    )


def send_slack_invite(token, team_domain, email):
    """
    Send invite via undocumented Slack API.
    """
    uri = f"https://{team_domain}.slack.com/api/users.admin.invite"
    response = requests.post(
        uri, data={"email": email, "token": token, "set_active": "true"}
    )
    result = response.json()
    logger.info("Invite response for %s: %s", email, result)
    return result


def update_invite_message(token, payload, new_attachment):
    """
    Update the original invite message with result.
    """
    original = payload.get("original_message", {})
    attachments = original.get("attachments", [])

    # Keep first two attachments, add result
    updated_attachments = attachments[:2] + [new_attachment]

    return {
        "token": token,
        "channel": payload["channel"]["id"],
        "ts": payload.get("message_ts"),
        "text": original.get("text", ""),
        "attachments": updated_attachments,
    }
