import os
from slack_bolt import App
from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler
import functions_framework

# Load Slack credentials from environment variables
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
print(f"SLACK_BOT_TOKEN: {slack_bot_token}")
print(f"SLACK_SIGNING_SECRET: {slack_signing_secret}")

if not slack_bot_token or not slack_signing_secret:
    raise ValueError("SLACK_BOT_TOKEN or SLACK_SIGNING_SECRET is missing in environment variables")


# Initialize the Slack app
app = App(token=slack_bot_token, signing_secret=slack_signing_secret)

# Respond to specific keywords
@app.event("message")
def handle_message_events(event, say):
    text = event.get("text", "").lower()
    user = event.get("user", "")

    if "hello" in text:
        say(f"Hi <@{user}>, how can I help you?")
    elif "thanks" in text:
        say(f"You're welcome, <@{user}>!")
    else:
        say(f"Hi <@{user}>, I noticed your message: {text}")

# Create the SlackRequestHandler for Google Cloud Functions
handler = SlackRequestHandler(app)

# Define the Google Cloud Function
@functions_framework.http
def slack_bot(request):
    return handler.handle(request)
