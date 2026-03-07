import fnmatch
import logging

from flask import Blueprint, current_app, jsonify, redirect, request

from app.buttons.invite import send_signup_prompt

signup_bp = Blueprint("signup", __name__)
logger = logging.getLogger(__name__)


@signup_bp.route("/signup", methods=["POST"])
def handle_signup():
    """
    Handle web signup requests.
    """
    data = request.form.to_dict()

    if not data:
        return jsonify({"error": "missing parameters"}), 400

    email = data.get("email")
    logger.info("Signup request: %s", email)

    if email and any(
        fnmatch.fnmatch(email, pat)
        for pat in current_app.config.get("BANNED_EMAILS", [])
    ):
        logger.info("Silently dropping banned email: %s", email)
        redirect_uri = data.get("redirect_uri")
        if redirect_uri:
            return redirect(redirect_uri)
        return "signup request sent", 200

    channel = current_app.config["SIGNUP_CHANNEL"]

    try:
        send_signup_prompt(channel, data)

        redirect_uri = data.get("redirect_uri")
        if redirect_uri:
            return redirect(redirect_uri)
        return "signup request sent", 200

    except Exception as e:
        logger.exception("Signup error")
        return jsonify({"msg": str(e)}), 500
