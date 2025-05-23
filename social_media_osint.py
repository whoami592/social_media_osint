# Social Media OSINT Framework for Kali Linux
# Developed for ethical hacking and open-source intelligence gathering
# Author: Inspired by ethical hacking principles
# Note: Ensure compliance with platform terms of service and legal regulations
# Requirements: Install tweepy, requests, instaloader, and beautifulsoup4
# Run: pip install tweepy requests instaloader beautifulsoup4

import tweepy
import requests
import instaloader
from bs4 import BeautifulSoup
import json
import sys
import argparse
from datetime import datetime

# Twitter API credentials (replace with your own)
TWITTER_API_KEY = "your_api_key"
TWITTER_API_SECRET = "your_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_TOKEN_SECRET = "your_access_token_secret"

def setup_twitter_api():
    """Set up Twitter API authentication."""
    try:
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api
    except Exception as e:
        print(f"Error setting up Twitter API: {e}")
        sys.exit(1)

def twitter_osint(username, api):
    """Gather public data from a Twitter profile."""
    try:
        user = api.get_user(screen_name=username)
        data = {
            "username": user.screen_name,
            "name": user.name,
            "followers": user.followers_count,
            "following": user.friends_count,
            "tweets": user.statuses_count,
            "location": user.location,
            "created_at": str(user.created_at),
            "bio": user.description
        }
        print(f"[+] Twitter data for {username}:")
        print(json.dumps(data, indent=2))
        return data
    except tweepy.TweepError as e:
        print(f"Error fetching Twitter data for {username}: {e}")
        return None

def instagram_osint(username):
    """Gather public data from an Instagram profile."""
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        data = {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "bio": profile.biography,
            "is_private": profile.is_private
        }
        print(f"[+] Instagram data for {username}:")
        print(json.dumps(data, indent=2))
        return data
    except Exception as e:
        print(f"Error fetching Instagram data for {username}: {e}")
        return None

def linkedin_osint(username):
    """Scrape public LinkedIn profile data (basic example)."""
    try:
        url = f"https://www.linkedin.com/in/{username}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error accessing LinkedIn profile for {username}")
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        data = {
            "username": username,
            "name": soup.find("h1", class_="text-heading-xlarge") or "N/A",
            "headline": soup.find("div", class_="text-body-medium") or "N/A"
        }
        print(f"[+] LinkedIn data for {username}:")
        print(json.dumps(data, indent=2))
        return data
    except Exception as e:
        print(f"Error fetching LinkedIn data for {username}: {e}")
        return None

def save_results(data, platform, username):
    """Save collected data to a JSON file."""
    if data:
        filename = f"osint_{platform}_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Social Media OSINT Framework for Kali Linux")
    parser.add_argument("-u", "--username", required=True, help="Target username")
    parser.add_argument("-p", "--platform", choices=["twitter", "instagram", "linkedin", "all"], default="all", help="Target platform")
    args = parser.parse_args()

    username = args.username
    platform = args.platform

    if platform in ["twitter", "all"]:
        twitter_api = setup_twitter_api()
        twitter_data = twitter_osint(username, twitter_api)
        save_results(twitter_data, "twitter", username)

    if platform in ["instagram", "all"]:
        instagram_data = instagram_osint(username)
        save_results(instagram_data, "instagram", username)

    if platform in ["linkedin", "all"]:
        linkedin_data = linkedin_osint(username)
        save_results(linkedin_data, "linkedin", username)

if __name__ == "__main__":
    main()