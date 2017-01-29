import text_analysis
from datetime import datetime

def handle_tweets(topic_ids, tweets):
    out = []
    for t in tweets:
        topic_ids, out = handle_tweet(topic_ids, out, t)
    return topic_ids, out

def handle_tweet(topic_ids, out, tweet):
    t_id = tweet['id']
    # Check if tweet already associated with topic
    if t_id in topic_ids:
        return topic_ids, out
    # Check for retweets
    if tweet.has_key('retweeted_status'):
        topic_ids, out = handle_tweet(topic_ids, out, tweer['retweeted_status'])
        # Compile Document
        c_tweet = {"retweet": True, "original": tweet['retweeted_status']['id']}
    else:
        text = tweet['text']
        c_tweet = {"retweet": False, "text": text}
        c_tweet.update(text_analysis.analysis(text))
    # Add common elements to the dictionary
    c_tweet.update({"_id": t_id, "date": make_date(tweet['date'])})
    out.append(c_tweet)
    return topic_ids, out

def make_date(raw):
    return datetime.strptime(raw, "%a %b %d %H:%M:%S +0000 %Y")
