from app.events.message import handle_message
from app.events.team_join import handle_team_join
from app.events.url_verification import handle_url_verification


def dispatch_event(event_type, data):
    """
    Route events to appropriate handlers.
    """
    handlers = {
        "url_verification": handle_url_verification,
        "team_join": handle_team_join,
        "message": handle_message,
    }

    handler = handlers.get(event_type)
    if not handler:
        raise ValueError(f"Unknown event type: {event_type}")

    return handler(data)
