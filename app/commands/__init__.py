import shlex

from app.commands.admin import handle_admin
from app.commands.join_private import handle_join_private
from app.commands.list_private import handle_list_private


def dispatch_command(command, text, context):
    """
    Route commands to appropriate handlers.
    """
    handlers = {
        "admin": handle_admin,
        "join-private": handle_join_private,
        "list-private": handle_list_private,
    }

    handler = handlers.get(command)
    if not handler:
        raise ValueError(f"Unknown command: {command}")

    # Parse arguments from text
    try:
        args = shlex.split(text) if text else []
    except ValueError:
        args = text.split() if text else []

    return handler(args, context)
