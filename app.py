import os
import random
import requests
import csv
import tweepy
from flask import Flask

app = Flask(__name__)

# --- CONFIGURATION ---

# Your public CSV link from Google Sheets
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSSaeSBT1QzO279wLHndPKaBOqABHMTTDAjE6mkyom3vuoMRF8gYRhPiWQgWiaD07G36PNnekVukoaO/pub?output=csv"

# Twitter API credentials (set these as environment variables)
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

def get_random_tweet(csv_url):
    response = requests.get(csv_url)
    lines = response.text.strip().split("\n")[1:]  # skip header
    tweets = [line.split(",")[0].strip().strip('"') for line in lines if line]
    return random.choice(tweets) if tweets else None

def post_to_twitter(tweet_text):
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_SECRET
    )
    api = tweepy.API(auth)
    api.update_status(tweet_text)

@app.route("/tweet", methods=["GET"])
def tweet():
    tweet_text = get_random_tweet(GOOGLE_SHEET_CSV_URL)
    if tweet_text:
        try:
            post_to_twitter(tweet_text)
            return {"status": "Tweet posted", "tweet": tweet_text}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    return {"error": "No tweet found"}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
