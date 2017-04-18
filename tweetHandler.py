import textAnalysis
import textClean
import pandas as pd

# Scans a tweet and records its topic
def scan(tweet, topic):
  text = textClean.clean(tweet['text'])
  if text == '':
    return None, None, None, None
  analysis = textAnalysis.analysis(text)
  if analysis is None:
    return None, None, None, None 
  scanned_tweet = {
    'id': tweet['id'],
    'topic': topic,
    'text': text.replace("'", ""),
    'username': tweet['username'],
    'p_words': analysis['p_count'],
    'n_words': analysis['n_count'],
    'rating': analysis['rating'],
    'retweets': tweet['retweets'],
    'date': tweet['date']
  }
  return scanned_tweet, analysis['words'], analysis['mentions'], analysis['tags']

# Scans and compiles the data of a large amount of tweets of a common topic
def handleTweets(tweets_in, topic):
  tweets = []
  words_list = [] #pd.DataFrame()
  mentions_list = [] #pd.DataFrame()
  tags_list = [] #pd.DataFrame()
  for t in tweets_in:
    scanned_tweet, words, mentions, tags = scan(t, topic)
    if scanned_tweet is not None:
      tweets.append(scanned_tweet)
      for tag, value in words.iteritems():
        words_list.append({'id': scanned_tweet['id'], 'topic': scanned_tweet['topic'], 'word':tag, 'count':value})
      for tag, value in mentions.iteritems():
        mentions_list.append({'id':scanned_tweet['id'], 'topic':scanned_tweet['topic'], 'mention':tag, 'count':value})
      for tag, value in tags.iteritems():
        tags_list.append({'id':scanned_tweet['id'], 'topic':scanned_tweet['topic'], 'tag':tag, 'count':value})
  return pd.DataFrame(tweets), pd.DataFrame(words_list), pd.DataFrame(mentions_list), pd.DataFrame(tags_list)