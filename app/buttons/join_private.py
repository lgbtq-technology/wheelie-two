import logging

from flask import current_app

from app.services.channel_service import get_private_channels
from app.services.slack_client import get_slack_client

logger = logging.getLogger(__name__)


def handle_join_private(payload):
    """
    Handle join-private button press from list.
    """
    client = get_slack_client(current_app.config["SLACK_BOT_TOKEN"])

    action = payload.get("actions", [{}])[0]
    channel_id = action.get("value")

    if not channel_id:
        return {
            "text": "A channel is required. Use `/list-private` to see a list of available private channels."
        }

    channels = get_private_channels()
    channel = next((c for c in channels if c["id"] == channel_id), None)

    if not channel:
        return {"text": "Bad channel id"}

    user_id = payload["user"]["id"]

    client.chat_postMessage(
        channel=channel["id"],
        text=f"Invite request from <@{user_id}>! Use `/invite <@{user_id}>` to accept (anyone here can do this)!",
    )

    return {
        "replace_original": True,
        "text": f"Invite request sent to #{channel['name']}",
    }
