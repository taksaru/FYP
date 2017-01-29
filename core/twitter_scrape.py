from TwitterSearch import *
# Source: https://github.com/ckoepp/TwitterSearch
import json

access_token = '787936570968043520-o1bHGOmR4AEuNoafsWoROAQIQIbwz3i'
access_token_secret = 's3vsnQAAuyLmhKYirZ0HIKRpreO8VsF84qAMDHfdmmmGG'
consumer_key = 'LJ0wq7eWPRSmdJVIoxQtYxyuy'
consumer_secret = 'CH811T3P1n7ofmPtd0POaML4vfGvKKIz7wLV212wKf3kRdp1i8'

def scrape_tweets(term):

    tso = TwitterSearchOrder()
    tso.set_keywords([term])
    tso.set_language('en')
    tso.set_link_filter()

    ts = TwitterSearch(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    return [t for t in ts.search_tweets_iterable(tso)]

'''
with open('tweets.json', 'w') as f:
    f.write(json.dumps(a, indent=2))
# set_supported_languages()
'''
