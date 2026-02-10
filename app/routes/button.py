import json
import logging

from flask import Blueprint, current_app, jsonify, request

from app.buttons import dispatch_button

button_bp = Blueprint("button", __name__)
logger = logging.getLogger(__name__)


@button_bp.route("/button", methods=["POST"])
def handle_button():
    """
    Handle interactive button callbacks from Slack.
    """
    # Parse payload from form data
    payload_str = request.form.get("payload", "{}")
    payload = json.loads(payload_str)

    # Verify token
    if payload.get("token") != current_app.config["SLACK_VERIFICATION_TOKEN"]:
        logger.error("Bad token in request")
        return jsonify({"error": "invalid verification token"}), 500

    callback_id = payload.get("callback_id", "").strip()

    try:
        response = dispatch_button(callback_id, payload)
        return jsonify(response), 200
    except ValueError as e:
        logger.error("No handler for button callback %s: %s", callback_id, e)
        return jsonify({"error": "no such event handler"}), 500
    except Exception as e:
        logger.exception("Unexpected button handler error: %s", e)
        return jsonify({"error": str(e)}), 500
