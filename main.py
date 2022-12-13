from dotenv import dotenv_values
from auth import handle_auth, create_api
import tweepy

def load_dotenv():
    env = dotenv_values('.env')

    # Load twitter key/secret from dotenv
    consumer_key = env['TWITTER_CONSUMER_KEY']
    consumer_secret = env['TWITTER_CONSUMER_SECRET']
    access_token, access_token_secret = "", ""

    try:
        access_token = env['ACCESS_TOKEN']
        access_token_secret = env['ACCESS_TOKEN_SECRET']
    except KeyError:
        print('Access token info does not exist in the dotenv file')
        access = handle_auth(consumer_key, consumer_secret)
        (access_token, access_token_secret) = access
    
    return (consumer_key, consumer_secret, access_token, access_token_secret)

def main():
    (consumer_key, consumer_secret, access_token, access_token_secret) = load_dotenv()
    # Auth and get api instance
    api = create_api(consumer_key, consumer_secret, access_token, access_token_secret)

if __name__ == "__main__":
    main()