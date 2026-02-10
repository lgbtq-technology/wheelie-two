import logging

from flask import current_app

from app.services.channel_service import get_private_channels
from app.services.slack_client import get_slack_client

logger = logging.getLogger(__name__)


def handle_join_private(args, context):
    """
    Request to join a private channel.
    """
    if not args:
        return {
            "text": "A channel is required. Use `/list-private` to see a list of available private channels."
        }

    channel_name = args[0].lstrip("#")
    user_id = context.get("user_id")

    client = get_slack_client(current_app.config["SLACK_BOT_TOKEN"])

    channels = get_private_channels()
    channel = next((c for c in channels if c["name"] == channel_name), None)

    if not channel:
        return {
            "text": f"#{channel_name} is not available through this command. Use `/list-private` to see a list of available channels."
        }

    # Build COC reference
    coc_url = current_app.config.get("COC_URL")
    coc_text = f"<{coc_url}|Code of Conduct>" if coc_url else "Code of Conduct"

    # Post request to channel
    client.chat_postMessage(
        channel=channel["id"],
        text=f"Invite request from <@{user_id}>! Use `/invite <@{user_id}>` to accept (anyone here can do this)!",
    )

    return {
        "text": (
            f"Join request sent. Please wait while the request is processed.\n\n"
            f"Remember that private channels are not for allies unless otherwise specified "
            f"and that there is a strong expectation of privacy in these channels -- "
            f"what is said in there stays there.\n\n"
            f"The {coc_text} still fully applies in these spaces, with some channel-specific "
            f"caveats (discussion of sexuality in lgbtq channels, for example)."
        )
    }
