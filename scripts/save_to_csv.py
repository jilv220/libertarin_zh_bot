import tweepy
import csv
import sys
sys.path.append('..')

from setup import load_dotenv
from datetime import datetime, timezone, timedelta

(consumer_key, consumer_secret, bearer_token, 
        access_token, access_token_secret, _) = load_dotenv('../.env')

# Client
client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key,
                consumer_secret=consumer_secret, access_token=access_token, 
                access_token_secret=access_token_secret, wait_on_rate_limit=True)

my_id = client.get_me().data.id

date_now = datetime.now(timezone.utc)
start_time = date_now - timedelta(hours=12)

response = client.get_users_tweets(
                        id = my_id, exclude=['retweets', 'replies'], 
                        start_time=start_time, tweet_fields=['created_at'],
                        max_results = 100
                    )

for tweet in response.data:
        print(tweet)
