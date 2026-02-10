import logging

from flask import Blueprint, current_app, jsonify, request

from app.events import dispatch_event

event_bp = Blueprint("event", __name__)
logger = logging.getLogger(__name__)


@event_bp.route("/event", methods=["POST"])
def handle_event():
    """
    Handle events from Slack Events API.
    """
    data = request.get_json()

    # Verify token
    if data.get("token") != current_app.config["SLACK_VERIFICATION_TOKEN"]:
        return jsonify({"error": "invalid verification token"}), 500

    # Handle URL verification challenge
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # Get event from wrapper or use data directly
    event = data.get("event", data)
    event_type = event.get("type", "")

    try:
        response = dispatch_event(event_type, data)
        return jsonify(response) if response else ("", 200)
    except ValueError as e:
        logger.error("No handler for event type %s: %s", event_type, e)
        return jsonify({"error": "no such event handler"}), 500
    except Exception as e:
        logger.exception("Unexpected event handler error %s", e)
        return jsonify({"error": "internal error"}), 500
