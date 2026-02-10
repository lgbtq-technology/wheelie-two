# Wheelie-Two

Wheelie-Two is a [Slack App](http://slack.com/apps) written as a replacement for the original [Wheelie](https://github.com/WeAllJS/wheelie-slack-app).

## Getting up and running

Wheelie-Two is a Docker container designed to run for a single Slack workspace. Configuration is done via environment variables.

### Initial Setup

1. Create a Slack App at https://api.slack.com/apps (click "build an app"). It will guide you through the inital flow and dump you on an app configuration page.
2. Copy `.env.example` to `.env` and fill in `APP_URL` (you must use https), and then `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, and `VERIFICATION_TOKEN` from the Slack app settings.
3. Go to the OAuth section of the app configuration and authorise `<APP_URL>/oauth` (e.g. `https://wheelie-two.aeracode.org/oauth`) as a valid redirect URL
4. Go to the Interactive Button page and set `<APP_URL>/button` as the URL
5. Go to the Slack Commands session and add commands for `/admin`, `/list-private`, and `/join-private` to all call `<APP_URL>/command`.
6. Run the app and visit `/install` to authorize the app in your workspace. It will send you to a page that shows you the values to set in `.env` for `SLACK_TEAM_ID`, `SLACK_TEAM_DOMAIN`, `SLACK_BOT_TOKEN`, and `SLACK_ACCESS_TOKEN`.
7. Visit `/install-inviter` to authorize an inviter user (required for sending workspace invites). Copy the resultant token into `SLACK_INVITE_TOKEN`.
8. Restart the app with all tokens configured
9. Invite the bot into the admin and admin-signup channels
