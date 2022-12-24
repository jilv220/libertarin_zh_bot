from logger import Logger
from datetime import datetime, timezone, timedelta
from tweet import Tweet
from translator import Translator
from setup import load_dotenv, load_config

import tweepy
import db
import random
import pandas as pd

logger = Logger('main')

def main():
    # Load config
    (twitter_handles, target_lang, translator_name) = load_config()
    logger.info(f'You are using {translator_name} as the translator')

    # Load dotenv
    (consumer_key, consumer_secret,
        bearer_token, access_token,
        access_token_secret, translator_token) = load_dotenv(translator=translator_name)

    # Init db
    con = db.connect()
    cur = con.cursor()

    try:
        res = db.create_tweets_table(cur)
    except Exception as e:
        logger.warning(e)

    # Client
    client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key,
                    consumer_secret=consumer_secret, access_token=access_token, 
                    access_token_secret=access_token_secret, wait_on_rate_limit=True)

    # Get ids from handle
    users = client.get_users(usernames = twitter_handles).data
    ids = [user.id for user in users]

    date_now = datetime.now(timezone.utc)

    # TODO: Make start_time configurable
    start_time = date_now - timedelta(hours=3)

    tweet_list = []
    for id in ids:
        response = client.get_users_tweets(
                        id = id, exclude=['retweets', 'replies'], 
                        start_time=start_time, tweet_fields=['created_at'],
                        media_fields=['media_key'], expansions=['attachments.media_keys'],
                        max_results = 20
                    )

        if response.data is None:
            # No latest tweets from this user, skip
            continue

        for tweet in response.data:
            is_media = tweet.text[:5] == 'https' and tweet.attachments
            tweet_list.append(Tweet(tweet.id, tweet.text, 
                True if is_media else False))

    # Remove quoted from tweet list
    res = cur.execute('SELECT tweet_id FROM tweets')
    quoted_ids = res.fetchall()
    quoted_ids = [item for sublist in quoted_ids for item in sublist]
    tweet_list = [tweet for tweet in tweet_list if tweet.id not in quoted_ids]

    # Randomnize the tweet_list
    random.shuffle(tweet_list)

    # Save to csv
    df = pd.DataFrame(data=[tweet.text for tweet in tweet_list if tweet.is_media is False], columns=['text'])
    df.to_csv('./data.csv', mode='w+')

    # Init translator
    translator = Translator(translator_name, translator_token)

    logger.info("Start tweeting process ...")
    for tweet in tweet_list:

        # Retweet instead if the tweet is pure media
        if (tweet.is_media):
            try:
                client.retweet(tweet_id=tweet.id)
            except Exception as e:
                logger.error(e)
            else:
                logger.info(f'id:{tweet.id} retweeted')
            continue

        translated_text = translator.translate_text(tweet.text, target_lang=target_lang)

        try:
            response = client.create_tweet(
                text=translated_text,
                quote_tweet_id= tweet.id
            )
            cur.execute('INSERT INTO tweets VALUES(?)', (tweet.id,))
        except Exception as e:
            logger.error(e)
        else:
            logger.info(f'id:{tweet.id} tweeted')

    logger.info("Tweeting process ends successfully!")

    # Commit transactions and close db
    con.commit()
    db.disconnect(con)
    logger.info("Database closed successfully!")


if __name__ == "__main__":
    main()
