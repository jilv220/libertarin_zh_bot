import sqlite3

def connect():
    con = sqlite3.connect("twitter_bot.db")
    return con

def create_tweets_table(cur):
    res = cur.execute(
        '''
        CREATE TABLE tweets(
            tweet_id PRIMARY KEY
        )
        ''')
    return res

def disconnect(con):
    con.close()