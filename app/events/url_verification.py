def handle_url_verification(data):
    """
    Respond to Slack URL verification challenge.
    """
    return {"challenge": data.get("challenge")}
