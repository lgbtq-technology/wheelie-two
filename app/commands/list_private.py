import logging
import re

from app.services.channel_service import get_private_channels

logger = logging.getLogger(__name__)


def handle_list_private(args, context):
    """
    List available private channels.
    """
    user_id = context.get("user_id")

    # Parse arguments
    filter_pattern = None
    show_all = False

    for arg in args:
        if arg == "--all":
            show_all = True
        elif not filter_pattern:
            filter_pattern = arg

    channels = get_private_channels(filter_pattern)

    # Filter to channels user is not in (unless --all)
    if not show_all:
        channels = [c for c in channels if user_id not in c.get("members", [])]

    if not channels:
        if filter_pattern:
            return {"text": f"No channels matching `{filter_pattern}`"}
        return {"text": "No private channels available"}

    return format_channel_list(filter_pattern, user_id, channels)


def format_channel_list(filter_pattern, user_id, channels):
    """
    Format channel list with join buttons.
    """
    attachments = []

    for chan in channels:
        purpose = chan.get("purpose", {}).get("value", "") or ""
        omit_count = "[no-count]" in purpose
        clean_purpose = re.sub(r"\[[^\]]*\]", "", purpose)

        members = chan.get("members", [])
        user_in_channel = user_id in members

        member_count = "?" if omit_count else str(len(members) - 1)
        title = f"#{chan['name']} [{member_count}]"

        text_parts = [clean_purpose]
        if user_in_channel:
            if clean_purpose:
                text_parts.append("(Already Joined)")
            else:
                text_parts = ["(Already Joined)"]

        attachment = {
            "title": title,
            "text": "\n".join(filter(None, text_parts)),
            "mrkdwn": True,
            "callback_id": "join-private",
        }

        if not user_in_channel:
            attachment["actions"] = [
                {"name": "join", "text": "Join", "type": "button", "value": chan["id"]}
            ]

        attachments.append(attachment)

    return {
        "text": "These channels are private to disallow previewing (view without join). Available private channels:",
        "attachments": attachments,
    }
