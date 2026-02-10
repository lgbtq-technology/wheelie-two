import logging

from flask import current_app

from app.services.slack_client import get_slack_client

logger = logging.getLogger(__name__)


def handle_admin(args, context):
    """
    Send a message to the admin channel.
    """
    if not args:
        return {"text": "Usage: /admin <message>"}

    message = " ".join(args)
    user_id = context.get("user_id")
    channel_name = context.get("channel_name")
    channel_id = context.get("channel_id")

    client = get_slack_client(current_app.config["SLACK_BOT_TOKEN"])

    # Format channel reference
    if channel_name == "directmessage":
        chan_ref = "a DM"
    elif channel_name == "privategroup":
        chan_ref = "a private channel"
    else:
        chan_ref = f"<#{channel_id}>"

    client.chat_postMessage(
        channel="admin", text=f"Message from <@{user_id}> in {chan_ref}:\n\n{message}"
    )

    return {"text": "Admins have been notified. They will respond as soon as possible."}
