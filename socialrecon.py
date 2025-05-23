# SocialRecon - Social Media Information Gathering Tool
# Coded by Mr. Sabaz Ali Khan, Pakistani Ethical Hacker
# For educational and ethical purposes only. Use with permission.

import argparse
import json
import tweepy
import instaloader
import requests
from bs4 import BeautifulSoup
import time
import sys
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Twitter API credentials (replace with your own)
TWITTER_API_KEY = "your_twitter_api_key"
TWITTER_API_SECRET = "your_twitter_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Initialize results dictionary
results = {}

def setup_twitter():
    """Set up Twitter API client."""
    try:
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api
    except Exception as e:
        print(f"[-] Twitter API setup failed: {e}")
        return None

def twitter_lookup(username, api):
    """Gather Twitter profile information."""
    try:
        user = api.get_user(screen_name=username)
        results["twitter"] = {
            "username": user.screen_name,
            "name": user.name,
            "bio": user.description,
            "followers": user.followers_count,
            "following": user.friends_count,
            "tweets": user.statuses_count,
            "location": user.location,
            "created_at": str(user.created_at)
        }
        print(f"[+] Twitter: Found profile for {username}")
    except tweepy.TweepError as e:
        results["twitter"] = {"error": f"Profile not found or private: {e}"}
        print(f"[-] Twitter: {e}")

def instagram_lookup(username):
    """Gather Instagram profile information."""
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        results["instagram"] = {
            "username": profile.username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "is_private": profile.is_private
        }
        print(f"[+] Instagram: Found profile for {username}")
    except Exception as e:
        results["instagram"] = {"error": f"Profile not found or private: {e}"}
        print(f"[-] Instagram: {e}")

def check_username_availability(username, platform):
    """Check if username exists on a platform via web scraping."""
    platforms = {
        "facebook": f"https://www.facebook.com/{username}",
        "linkedin": f"https://www.linkedin.com/in/{username}",
        "pinterest": f"https://www.pinterest.com/{username}"
    }
    if platform not in platforms and platform != "all":
        print(f"[-] Unsupported platform: {platform}")
        return

    if platform == "all":
        target_platforms = platforms
    else:
        target_platforms = {platform: platforms[platform]}

    for plat, url in target_platforms.items():
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                results[plat] = {"status": "likely exists"}
                print(f"[+] {plat.capitalize()}: Username {username} likely exists")
            else:
                results[plat] = {"status": "not found"}
                print(f"[-] {plat.capitalize()}: Username {username} not found")
            time.sleep(1)  # Respect rate limits
        except Exception as e:
            results[plat] = {"error": str(e)}
            print(f"[-] {plat.capitalize()}: Error - {e}")

def save_results(output_file):
    """Save results to a JSON file."""
    try:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
        print(f"[+] Results saved to {output_file}")
    except Exception as e:
        print(f"[-] Failed to save results: {e}")

def main():
    parser = argparse.ArgumentParser(description="SocialRecon - Social Media OSINT Tool by Mr. Sabaz Ali Khan")
    parser.add_argument("-u", "--username", required=True, help="Target username")
    parser.add_argument("-p", "--platform", default="all", help="Platform (twitter, instagram, facebook, linkedin, pinterest, all)")
    parser.add_argument("-o", "--output", default="results.json", help="Output JSON file")
    args = parser.parse_args()

    print("=====================================")
    print("SocialRecon by Mr. Sabaz Ali Khan")
    print("Ethical Hacking Tool - Use Responsibly")
    print("=====================================")

    if args.platform in ["twitter", "all"]:
        twitter_api = setup_twitter()
        if twitter_api:
            twitter_lookup(args.username, twitter_api)

    if args.platform in ["instagram", "all"]:
        instagram_lookup(args.username)

    if args.platform in ["facebook", "linkedin", "pinterest", "all"]:
        check_username_availability(args.username, args.platform)

    save_results(args.output)

if __name__ == "__main__":
    main()