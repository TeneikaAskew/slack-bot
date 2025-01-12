import os
from slack_bolt import App
from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler
import functions_framework

# Load Slack credentials from environment variables
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

if not slack_bot_token or not slack_signing_secret:
    raise ValueError("SLACK_BOT_TOKEN or SLACK_SIGNING_SECRET is missing in environment variables")

# Initialize the Slack app
app = App(token=slack_bot_token, signing_secret=slack_signing_secret)

# Respond to specific keywords in a thread
@app.event("message")
def handle_message_events(event, say):
    text = event.get("text", "").lower()  # Normalize the message text to lowercase
    thread_ts = event.get("ts")  # Use the timestamp of the original message

    # Define keywords for each category, all in lowercase for consistency
    socials_keywords = ["linkedin", "x", "twitter"]
    support_keywords = ["help", "recording", "recordings", "broken", "not working"]
    timing_keywords = ["time", "training start", "class start", "meeting time", "meet"]

    # Check which category the message matches
    if any(keyword in text for keyword in socials_keywords):
        say("Please share your socials in #networking so it doesn't get lost in the feed.", thread_ts=thread_ts)
    elif any(keyword in text for keyword in support_keywords):
        say("Check the #ai-automation-support channel for all recordings and program announcements.", thread_ts=thread_ts)
    elif any(keyword in text for keyword in timing_keywords):
        say("Check your email for your workshop start times!", thread_ts=thread_ts)
    else:
        say(f"Hi <@{event.get('user', '')}>, I noticed your message: {text}", thread_ts=thread_ts)

# Create the SlackRequestHandler for Google Cloud Functions
handler = SlackRequestHandler(app)

# Define the Google Cloud Function
@functions_framework.http
def slack_bot(request):
    return handler.handle(request)
