import tweepy
from datetime import datetime

# Replace 'YOUR_CONSUMER_KEY', 'YOUR_CONSUMER_SECRET', 'YOUR_ACCESS_TOKEN', and 'YOUR_ACCESS_TOKEN_SECRET'
# with your actual Twitter API credentials
CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

def setup_twitter_api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def post_tweet(api):
    tweet_text = "Hello, world! This is a test tweet from my social media bot."
    api.update_status(status=tweet_text)
    print(f"Tweet posted successfully at {datetime.now()}")

def main():
    twitter_api = setup_twitter_api()
    post_tweet(twitter_api)

if __name__ == '__main__':
    main()