import text_analysis
import twitter-scrape
import json

# Topic used for analysis
topic = 'Overwatch'


tweets = twitter_scrape.scrape_tweets(topic)
tweet_ids = mongo_interface.pull_topic(topic)
tweet_ids, compiled_tweets = tweet_analysis.analyze(tweet_ids, tweets)
mongo_interface.add_tweets(topic, tweet_ids, compiled_tweets)
out = mongo_interface.pull_tweets(topic)
