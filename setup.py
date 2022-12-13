from dotenv import dotenv_values
from auth import handle_auth
from exceptions import EnvEmptyValue

import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

def load_dotenv(path):
    env = dotenv_values(path)

    try:
        consumer_key = env['TWITTER_CONSUMER_KEY']
        consumer_secret = env['TWITTER_CONSUMER_SECRET']
        bearer_token = env['BEARER_TOKEN']
    except KeyError:
        logger.error('Missing Twitter authentication entries from the dotenv file')
        exit()

    try:
        deepl_auth_key = env['DEEPL_AUTH_KEY']
    except KeyError:
        logger.error('Missing DEEPL authentication key entry from the dotenv file')
        exit()

    try:
        access_token = env['ACCESS_TOKEN']
        access_token_secret = env['ACCESS_TOKEN_SECRET']
    except KeyError:
        logger.error('Missing Twitter access entries from the dotenv file')
        access = handle_auth(consumer_key, consumer_secret)
        (access_token, access_token_secret) = access

    if '' in (consumer_key, consumer_secret, bearer_token, 
    access_token, access_token_secret):
        raise EnvEmptyValue()
    
    return (consumer_key, consumer_secret, bearer_token, 
    access_token, access_token_secret, deepl_auth_key)

def load_config():
    f = open('config.json')
    data = json.load(f)
    f.close()
    return (data['handles'], data['target-language'])