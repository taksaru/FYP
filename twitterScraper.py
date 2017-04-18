from twython import Twython
from datetime import datetime
# Source: https://github.com/ckoepp/TwitterSearch

access_token = '787936570968043520-o1bHGOmR4AEuNoafsWoROAQIQIbwz3i'
access_token_secret = 's3vsnQAAuyLmhKYirZ0HIKRpreO8VsF84qAMDHfdmmmGG'
consumer_key = 'LJ0wq7eWPRSmdJVIoxQtYxyuy'
consumer_secret = 'CH811T3P1n7ofmPtd0POaML4vfGvKKIz7wLV212wKf3kRdp1i8'

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

# Scrapes the 'amount' tweets on topic 'keyword'
def scrapeTweets(keyword, amount):
  try:
    return [tweetFormat(t) for t in twitter.search(q=keyword, count=amount, lang='en', include_entities=False)['statuses']]
  except:
    return []

'''
{
  "id",
  "username",
  "retweets",
  "date"
}
'''
# Simplifies data in the tweet
def tweetFormat(tweet):
  out = {
    'id': tweet['id'],
    'text': tweet['text'],
    'username': tweet['user']['screen_name'],
    'retweets': tweet['retweet_count'],
    'date': dateFormat(tweet['created_at'])
  }
  return out

# Parses a date from the standard Twitter Date String
def dateFormat(dateString):
  # "Mon Dec 26 13:08:33 +0000 2016"
  dt = datetime.strptime(dateString, '%a %b %d %H:%M:%S +0000 %Y')
  return dt.strftime('%Y-%m-%d %H:%M:%S')
