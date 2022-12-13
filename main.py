from auth import create_api
from datetime import datetime, timezone, timedelta
from tweet import Tweet
from setup import load_dotenv, load_config

import tweepy
import deepl
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

def main():
    # Load dotenv
    (consumer_key, consumer_secret, bearer_token, 
        access_token, access_token_secret, deepl_auth_key) = load_dotenv('.env')

    # Load config
    (twitter_handles, target_language) = load_config()

    # Auth and get api instance
    api = create_api(consumer_key, consumer_secret, access_token, access_token_secret)

    # Client
    client = tweepy.Client(bearer_token)

    # Get ids from handle
    users = api.lookup_users(screen_name = twitter_handles)
    ids = [user.id for user in users]

    date_now = datetime.now(timezone.utc)
    one_day_before = date_now - timedelta(days=1)

    tweet_list = []
    for id in ids:
        response = client.get_users_tweets(
                        id = id, exclude=['retweets', 'replies'], 
                        start_time=one_day_before, tweet_fields=['created_at'],
                        media_fields=['media_key'], expansions=['attachments.media_keys']
                    )
        
        if response.data is None:
            # No latest tweets from this user, skip
            continue

        for tweet in response.data:
            tweet_list.append(Tweet(tweet.id, tweet.text))

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    # Init translator
    translator = deepl.Translator(deepl_auth_key)

    for tweet in tweet_list:
        # Need to handle possible exceptions here
        translated_text = translator.translate_text(tweet.text, target_lang=target_language).text
        response = client.create_tweet(
            text=translated_text,
            quote_tweet_id= tweet.id
        )

if __name__ == "__main__":
    main()