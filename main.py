from dotenv import dotenv_values
from auth import handle_auth
import tweepy

env = dotenv_values('.env')

# Load twitter key/secret from dotenv
consumer_key = env['TWITTER_CONSUMER_KEY']
consumer_secret = env['TWITTER_CONSUMER_SECRET']

try:
    access_token = env['ACCESS_TOKEN']
    access_token_secret = env['ACCESS_TOKEN_SECRET']
except KeyError:
    print('Access info does not exist in the dotenv file')
    access = handle_auth(consumer_key, consumer_secret)
    (access_token, access_token_secret) = access

# Auth and get api instance
auth = tweepy.OAuth1UserHandler(
   consumer_key, 
   consumer_secret, 
   access_token, 
   access_token_secret
)
api = tweepy.API(auth)

# Make a new tweet
api.update_status('Hello, world! I am a bot.')