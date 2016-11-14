import json

def handle_tweet(tweet):
    output = {}
    if tweet['retweeted']:
        if tweet_exists(tweet['retweeted_status']['id']):
            add_retweet(tweet)
    output['_id'] = tweet['id']

def db_exists(id):
    return

def insert_tweet(tweet):
    return

def add_retweet(tweet):
    return
