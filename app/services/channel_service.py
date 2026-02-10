import logging
import re

from flask import current_app

from app.services.slack_client import get_slack_client

logger = logging.getLogger(__name__)


def get_private_channels(filter_pattern=None):
    """
    Get list of private channels the bot is in.

    Excludes admin channels and those marked [secret].
    """
    client = get_slack_client(current_app.config["SLACK_BOT_TOKEN"])

    # Build regex filter
    if filter_pattern:
        try:
            regex = re.compile(filter_pattern, re.IGNORECASE)
        except re.error:
            regex = re.compile(re.escape(filter_pattern), re.IGNORECASE)
    else:
        regex = re.compile(".*")

    # Get private channels
    response = client.conversations_list(types="private_channel", exclude_archived=True)

    channels = []
    for channel in response.get("channels", []):
        name = channel.get("name", "")
        purpose = channel.get("purpose", {}).get("value", "") or ""

        # Apply filters - exclude admin channels and secret channels
        if name.lower().startswith("admin"):
            continue
        if "[secret]" in purpose.lower():
            continue

        # Match against filter (name, #name, or purpose)
        if not (
            regex.search(name) or regex.search(f"#{name}") or regex.search(purpose)
        ):
            continue

        # Get members for this channel
        try:
            members_response = client.conversations_members(channel=channel["id"])
            channel["members"] = members_response.get("members", [])
        except Exception as e:
            logger.warning("Could not get members for %s: %s", name, e)
            channel["members"] = []

        channels.append(channel)

    return channels
