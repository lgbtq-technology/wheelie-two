import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


def get_slack_client(token):
    """
    Create a Slack WebClient with the given token.
    """
    return WebClient(token=token)


def safe_api_call(client, method, **kwargs):
    """
    Wrapper for Slack API calls with error handling.
    """
    try:
        api_method = getattr(client, method)
        return api_method(**kwargs)
    except SlackApiError as e:
        logger.error("Slack API error calling %s: %s", method, e.response["error"])
        raise
