import tweepy
import csv
import sys
sys.path.append('..')

from setup import load_dotenv
from auth import create_api

(consumer_key, consumer_secret, bearer_token, 
        access_token, access_token_secret, deepl_auth_key) = load_dotenv('../.env')

api = create_api(consumer_key, consumer_secret, access_token, access_token_secret)

