import os


class Config:
    """
    Base configuration.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # Slack app credentials
    SLACK_CLIENT_ID = os.environ.get("SLACK_CLIENT_ID")
    SLACK_CLIENT_SECRET = os.environ.get("SLACK_CLIENT_SECRET")
    SLACK_VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN")

    # Slack team settings (single team mode)
    SLACK_TEAM_ID = os.environ.get("SLACK_TEAM_ID")
    SLACK_TEAM_DOMAIN = os.environ.get("SLACK_TEAM_DOMAIN")
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_ACCESS_TOKEN = os.environ.get("SLACK_ACCESS_TOKEN")
    SLACK_INVITE_TOKEN = os.environ.get("SLACK_INVITE_TOKEN")

    # App settings
    APP_URL = os.environ.get("APP_URL", "http://localhost:5000")
    SIGNUP_CHANNEL = os.environ.get("SIGNUP_CHANNEL", "admin-signups")
    COC_URL = os.environ.get("COC_URL")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
