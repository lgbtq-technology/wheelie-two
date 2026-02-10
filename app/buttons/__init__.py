from app.buttons.invite import handle_invite
from app.buttons.join_private import handle_join_private


def dispatch_button(callback_id, payload):
    """
    Route button callbacks to appropriate handlers.
    """
    handlers = {
        "invite": handle_invite,
        "join-private": handle_join_private,
    }

    handler = handlers.get(callback_id)
    if not handler:
        raise ValueError(f"Unknown callback_id: {callback_id}")

    return handler(payload)
