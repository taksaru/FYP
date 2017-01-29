import json
import text_analysis
# Remove Later
import random


positive_file = open("text/positive.txt").read()
positive_words = positive_file.split('\n')

negative_file = open('text/negative.txt').read()
negative_words=negative_file.split('\n')

def handle_tweet(tweet):
    output = {}
    tweet_id = tweet['id']
    # tweet['retweeted'] is depreciated
    # Non retweets have retweeted_status
    if tweet.has_key("retweeted_status"):
        if tweet['retweeted_status']['id'] in topic_ids:
            print 'RETWEET EXISTS'
            add_retweet(tweet)
        else:
            print 'CREATING RETWEET DOC'
            handle_tweet(tweet['retweeted_status'])
    if tweet_exists(tweet_id):
        print 'TWEET exists'
    else:
        document_tweet(tweet)

def document_tweet(tweet):
    text = tweet['text']
    analysis = text_analysis.analysis(text)
    tweet_doc = {'_id': tweet['id'],
        'text': text,
        'retweet_count': 0,
        'retweet_ids': [],
        'rating': analysis['rating'],
        'p_count': analysis['p_count'],
        'positive_words': analysis['positive_words'],
        'n_count': analysis['n_count'],
        'negative_words': analysis['negative_words'],
        'results': analysis['results']
    }
    insert_tweet(tweet_doc)

def tweet_exists(tweet_id):
    rng = random.randint(0,1)
    print 'RNG: ' + str(rng)
    if rng == 0:
        print 'Tweet ' + str(tweet_id) + ' exists'
        return True
    print 'Tweet ' + str(tweet_id) + ' does not exist'
    return False

def insert_tweet(tweet):
    print 'ADDED TWEET ' + str(tweet['_id'])
    return

def add_retweet(tweet):
    print 'ADDED RETWEET ' + str(tweet['id'])
    return
