import tweepy

from logger import Logger
logger = Logger(__name__)

def handle_auth(consumer_key, consumer_secret):
    # Create an OAuthHandler instance
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret,
    callback="oob")

    # Get the request token
    auth_url = auth.get_authorization_url()

    # Prompt the user to visit the authorization URL and enter the verification code
    print('Please visit this URL to authorize: ' + auth_url)
    verification_code = input('Enter the verification code: ')

    # Get the access token
    auth.get_access_token(verification_code)

    # Print the access token and secret
    print('Access token: ' + auth.access_token)
    print('Access token secret: ' + auth.access_token_secret)

    return (auth.access_token, auth.access_token_secret)