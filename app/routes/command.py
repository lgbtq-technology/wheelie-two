import logging

from flask import Blueprint, current_app, jsonify, request

from app.commands import dispatch_command

command_bp = Blueprint("command", __name__)
logger = logging.getLogger(__name__)


@command_bp.route("/command", methods=["POST"])
def handle_command():
    """
    Handle slash commands from Slack.
    """
    data = request.form.to_dict()

    # Verify token
    if data.get("token") != current_app.config["SLACK_VERIFICATION_TOKEN"]:
        logger.warning("Bad verification token: %s", data.get("token"))
        return jsonify({"error": "invalid verification token"}), 401

    # Extract command info
    command = data.get("command", "").lstrip("/")
    text = data.get("text", "")

    logger.info(
        "User %s (team: %s) invoked command: %s %s",
        data.get("user_name"),
        data.get("team_id"),
        command,
        text,
    )

    try:
        response = dispatch_command(command, text, data)
        return jsonify(response), 200
    except ValueError as e:
        return jsonify({"text": str(e)}), 200
    except Exception as e:
        logger.exception("Unexpected command error")
        return jsonify({"error": str(e)}), 500
