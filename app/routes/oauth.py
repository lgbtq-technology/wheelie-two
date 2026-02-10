import logging

from flask import Blueprint, current_app, request
from slack_sdk import WebClient

oauth_bp = Blueprint("oauth", __name__)
logger = logging.getLogger(__name__)


@oauth_bp.route("/oauth")
def oauth_callback():
    """
    Handle OAuth callback from Slack.

    Displays tokens for the user to copy into environment variables.
    """
    code = request.args.get("code")
    if not code:
        return {"error": "Missing authorization code"}, 400

    client = WebClient()

    try:
        # Exchange code for tokens
        response = client.oauth_access(
            client_id=current_app.config["SLACK_CLIENT_ID"],
            client_secret=current_app.config["SLACK_CLIENT_SECRET"],
            code=code,
        )

        if not response.get("access_token"):
            return {"error": "No access token granted"}, 400

        # Get team info
        auth_client = WebClient(token=response["access_token"])
        auth_response = auth_client.auth_test()

        # Extract domain from URL (e.g., https://team.slack.com/ -> team)
        url = auth_response.get("url", "")
        domain = url.replace("https://", "").replace(".slack.com/", "").rstrip("/")

        # Check if this is an inviter setup (client scope)
        scope = response.get("scope", "")
        if "client" in scope:
            # Inviter setup - show invite token
            logger.info("Inviter setup completed")
            html = f"""
            <h2>Inviter Authorization Complete!</h2>
            <p>Add this to your environment variables:</p>
            <pre>SLACK_INVITE_TOKEN={response["access_token"]}</pre>
            <p>Then restart the application.</p>
            """
        else:
            # Regular app setup - show all tokens
            logger.info("App setup completed")
            bot = response.get("bot", {})
            html = f"""
            <h2>Authorization Complete!</h2>
            <p>Add these to your environment variables:</p>
            <pre>
SLACK_TEAM_ID={response.get("team_id", "")}
SLACK_TEAM_DOMAIN={domain}
SLACK_ACCESS_TOKEN={response["access_token"]}
SLACK_BOT_TOKEN={bot.get("bot_access_token", "")}
            </pre>
            <p>Then restart the application.</p>
            <p><a href="/install-inviter">Click here</a> to also set up an inviter user (required for sending workspace invites).</p>
            """

        return html, 200, {"Content-Type": "text/html"}

    except Exception as e:
        logger.exception("OAuth error")
        return {"error": str(e)}, 500
