import tweet_handling
import json

tweets = json.loads(open("tweets2.json").read())

for t in tweets:
    tweet_handling.handle_tweet(t)
