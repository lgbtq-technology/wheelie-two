import logging

logger = logging.getLogger(__name__)


def handle_team_join(data):
    """NOOP - Log when users join team."""
    logger.info("New user joined team: %s", data)
    return None
