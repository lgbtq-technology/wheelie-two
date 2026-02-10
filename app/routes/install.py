from flask import Blueprint, current_app, request

install_bp = Blueprint("install", __name__)

OAUTH_SCOPES = ["incoming-webhook", "commands", "bot", "chat:write:user"]


@install_bp.route("/install")
def install():
    """
    Render Add to Slack button.
    """
    client_id = current_app.config["SLACK_CLIENT_ID"]
    scopes = ",".join(OAUTH_SCOPES)

    html = f"""
    <h2>Install Wheelie-Two</h2>
    <p>Click the button below to install the app and get your OAuth tokens.</p>
    <p>After authorization, you'll see the tokens to add to your environment variables.</p>
    <a href="https://slack.com/oauth/authorize?client_id={client_id}&scope={scopes}">
        <img alt="Add to Slack" height="40" width="139"
             src="https://platform.slack-edge.com/img/add_to_slack.png"
             srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x,
                     https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" />
    </a>
    """
    return html, 200, {"Content-Type": "text/html"}


@install_bp.route("/install-inviter")
def install_inviter():
    """
    Render inviter authorization link.
    """
    client_id = current_app.config["SLACK_CLIENT_ID"]
    team = request.args.get("team", current_app.config.get("SLACK_TEAM_ID", ""))

    params = f"client_id={client_id}&scope=client&team={team}"
    html = f"""
    <h2>Authorize Inviter</h2>
    <p>Click below to authorize a user who can send workspace invites.</p>
    <p>After authorization, you'll see the invite token to add to your environment variables.</p>
    <a href="https://slack.com/oauth/authorize?{params}">Click here to authorize an inviter user</a>
    """
    return html, 200, {"Content-Type": "text/html"}
