import MySQLdb
import pandas as pd
import textAnalysis
import numpy as np
'''Create Tables
  CREATE TABLE tweets (
    id VARCHAR(20) PRIMARY KEY,
    text VARCHAR(200),
    p_words SMALLINT,
    n_words SMALLINT,
    rating FLOAT,
    username VARCHAR(25),
    retweets INT,
    date DATETIME
  );

  CREATE TABLE topics (
    topic VARCHAR(25),
    tweet_id VACHAR(20),
    PRIMARY KEY(topic, tweet_id)
  );

  CREATE TABLE word_counts (
    topic VARCHAR(25),
    word VARCHAR(100),
    count INT,
    PRIMARY KEY (topic, word)
  );

  CREATE TABLE mentions (
    topic VARCHAR(25),
    mention VARCHAR(100),
    count INT,
    PRIMARY KEY (topic, mention)
  );

  CREATE TABLE tags (
    topic VARCHAR(25),
    tag VARCHAR(255),
    count INT,
    PRIMARY KEY (topic, tag)
  );

  CREATE TABLE clients (
    topic VARCHAR(25) PRIMARY KEY,
    rate INT,
    amount INT
  );

'''

# Convert SQL Data to Pandas DataFrame
def toDF(data):
  out = []
  for row in data:
    out.append(row)
  return pd.DataFrame(out)

# String to datetime formatter
def toDate(dateString):
  try:
    return datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
  except TypeError:
    return dateString

# Generates WHERE clause depending on dates given/not given in an API Call
def dateRange(before, after):
  if after == '':
    # All data before a certain date
    if before != '':
      return  "date < '%s' " % before
  else:
    # All data after a certain date
    if before == '':
      return "date > '%s' " % after
    # All data between two dates
    else:
      return "date BETWEEN '%s' AND '%s' " % (before, after)
  return ''

# Converts list of items into a large tuple
def tupleList(in_list):
  in_list = list(set(in_list))
  out = '('
  out += "'%s'" % str(in_list[0])
  for item in in_list[1:]:
    out += ",'%s'" % item
  out += ')'
  return out

# Database Class
class MyDB():

  # Initialise Database and cursor
  def __init__(self):
    self.db = MySQLdb.connect("localhost","wop","password","FYP" )
    self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

  # Add tweets to Database
  def addTweets(self, tweet_df, word_counts, mentions, tags):
    # 1. Add raw tweets to tweets table
    tweet_rows = tweet_df[['id', 'text', 'p_words', 'n_words', 'rating',
      'username', 'retweets', 'date']].to_dict('records')
    query = "INSERT INTO tweets (id, text, p_words, n_words, rating, username, retweets, date) VALUES "
    for row in tweet_rows:
      row['text'] = row['text'].replace("'", '')
      if len(row['text']) < 200:
        query += "(%s, '%s', %s, %s, %s, '%s', %s, '%s')," % (
          row['id'], row['text'].replace("'", ""), row['p_words'], row['n_words'],
          row['rating'], row['username'], row['retweets'], row['date'])
    query = query[:-1]
    query += ' ON DUPLICATE KEY UPDATE id = id, retweets = VALUES(retweets);'

    try:
      self.cursor.execute(query)
      self.db.commit()
    except MySQLdb.Error, e:
      print query
      raise
    topic_df = tweet_df[['id', 'topic']]

    # 1.5 Get current stored ids for Word Count and Mentions to  avoid duplication
    query = """SELECT DISTINCT tweet_id FROM topics
      WHERE topic IN %s AND tweet_id IN %s;""" % (
        tupleList(topic_df['topic'].values),
        tupleList(topic_df['id'].values))

    self.cursor.execute(query)
    ids = self.cursor.fetchall()

    self.db.commit()
    # Clean list of unique matching ids
    ids = [d['tweet_id'] for d in ids]

    # 2 Add Word count to DB word_counts table
    if len(word_counts) > 0:
      word_counts = word_counts[~word_counts.id.isin(ids)]
      word_counts = word_counts.to_dict('records')
      query = "INSERT INTO word_counts (topic, word, count) VALUES "
      for row in word_counts:
        if len(row['word']) <= 100 and row['word'] != '':
          query += "('%s', '%s', %s)," % (row['topic'], row['word'], row['count'])
      query = query[:-1]
      # Increase counter by given count
      query += ' ON DUPLICATE KEY UPDATE count = count + VALUES(count);'

      self.cursor.execute(query)
      self.db.commit()

    # 3 Add Mentions to DB mentions table
    if len(mentions) > 0:
      mentions = mentions[~mentions.id.isin(ids)]
      mentions = mentions.to_dict('records')
      query = "INSERT INTO mentions (topic, mention, count) VALUES"
      for row in mentions:
        if row['mention'] != '' or len(row['mention']) < 50:
          query += "('%s', '%s', %s)," % (row['topic'], row['mention'], row['count'])
      query = query[:-1]
      # Increase counter by given count
      query += ' ON DUPLICATE KEY UPDATE count = count + VALUES(count);'

      self.cursor.execute(query)
      self.db.commit()

    # 4 Add tags to DB tags table
    if len(tags) > 0:
      tags = tags[~tags.id.isin(ids)]
      tags = tags.to_dict('records')
      query = "INSERT INTO tags (topic, tag, count) VALUES"
      for row in tags:
        if row['tag'] != '':
          query += "('%s', '%s', %s)," % (row['topic'], row['tag'], row['count'])
      query = query[:-1]
      # Increase counter by given count
      query += ' ON DUPLICATE KEY UPDATE count = count + VALUES(count);'

      self.cursor.execute(query)
      self.db.commit()

    # 4 Insert tweets into topic db for grouping
    topic_df = tweet_df[['id', 'topic']]
    topic_rows = topic_df.to_dict('records')
    query = 'INSERT INTO topics (topic, tweet_id) VALUES'
    for row in topic_rows:
      query += "('%s', '%s')," % (row['topic'], row['id'])
    query = query[:-1]
    # Ignore duplicates
    query += ' ON DUPLICATE KEY UPDATE tweet_id = tweet_id;'

    self.cursor.execute(query)
    self.db.commit()

  # Get All Clients in the database
  def getClients(self):
    query = 'SELECT topic, rate, amount FROM clients;'
    self.cursor.execute(query)
    df = toDF(self.cursor.fetchall())
    return df

  # Add new client to database
  def storeClient(self, client):
    query = 'INSERT INTO clients VALUES (%s, %s, %s);'
    self.cursor.execute(query, (client['topic'], client['rate'], client['amount']))
    self.db.commit()

  # Get all tweets from the databse on a given topic between given dates
  def getData(self, topic, before, after):
    query = """SELECT * FROM tweets WHERE id IN (
      SELECT DISTINCT tweet_id FROM topics WHERE topic = %s) """
    dateClause = dateRange(before, after)
    if dateClause != '':
      query += 'WHERE %s' % dateClause
    query += ';' 
    self.cursor.execute(query, (topic,))
    df = toDF(self.cursor.fetchall())
    return df

  # Gathers compiled tweets on a given topic within between given dates, can be grouped hourly and/or weighed
  def viewProgress(self, topic, hour, weight, before, after):
    self.cursor.execute("SET sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'")
    self.db.commit()
    dateClause = dateRange(before, after)
    # Weight = every tweet's rating is multiplied by its retweets divided by the average retweets for that day/hour
    if weight:
      if hour:
        query = """SELECT date, rating FROM (
          

          SELECT t1.d2 AS date, AVG(rating * ((t1.retweets+1)/t2.ar)) AS rating FROM
          (
            SELECT date AS d2, rating, retweets FROM tweets 
            WHERE id IN (SELECT tweet_id FROM topics WHERE topic = %s)
          )AS t1 JOIN (
            # Get average retweets per hour
            SELECT date, AVG(retweets) AS ar FROM tweets
            WHERE id IN (SELECT tweet_id FROM topics WHERE topic = %s)
            GROUP BY DATE(date), HOUR(date)
          ) AS t2 ON t1.d2 = t2.date
          GROUP BY DATE(t1.d2), HOUR(t1.d2)
        ) AS t
        WHERE rating <> 0 """
      else:
        query = """SELECT date, rating FROM (
        # Average rating times retweets divided by average retweets for that date
        SELECT t1.d2 AS date, AVG(rating * ((t1.retweets)/t2.ar)) AS rating FROM
        (
          SELECT date AS d2, rating, retweets FROM tweets 
          WHERE id IN (SELECT tweet_id FROM topics WHERE topic = %s)
        )AS t1 JOIN (
          # Get average retweets per day
          SELECT date, AVG(retweets) AS ar FROM tweets
          WHERE id IN (SELECT tweet_id FROM topics WHERE topic = %s)
          GROUP BY DATE(date)
        ) AS t2 ON t1.d2 = t2.date
        GROUP BY DATE(t1.d2)
      ) AS t
      WHERE rating <> 0 """
      if dateClause != '':
        query += 'AND %s' % dateClause
      self.cursor.execute(query, (topic, topic))
    else:
      # Returns dates and average rating with requested grouping
      query = """SELECT date, AVG(rating) AS rating FROM tweets 
      WHERE id IN (SELECT tweet_id FROM topics WHERE topic = %s)"""
      if dateClause != '':
        query += 'AND %s ' % dateClause
      query += 'GROUP BY DATE(date)'
      if hour:
        query += ', HOUR(date)'
      self.cursor.execute(query, (topic,))
    df = toDF(self.cursor.fetchall())
    if len(df) == 0:
      return None
    return df

  # Reloads the textAnalysis and rescans all tweets in the database with the updated analysis
  def reScan(self):
    # Reloads module
    reload(textAnalysis)
    start = 'INSERT INTO tweets (id, p_words, n_words, rating) VALUES '
    count = 0
    end = ' ON DUPLICATE KEY UPDATE p_words=VALUES(p_words), n_words=VALUES(n_words), rating=VALUES(rating);'
    cursor = self.cursor
    db = self.db
    print 'Collecting all tweets'
    query = 'SELECT id, text FROM tweets;'
    self.cursor.execute(query)
    data = self.cursor.fetchall()
    print 'All tweets Collected'
    query = '' + start
    print 'Re-scanning tweets'
    for row in data:
      count += 1
      scan = textAnalysis.analysis(row['text'])
      query += '(%s, %s, %s, %s),' % (row['id'], scan['p_count'], scan['n_count'], scan['rating'])
      # Inserts the updated tweets in batches of 500,000
      if count == 500000:
        query = query[:-1]
        query += end
        cursor.execute(query)
        db.commit()
        query = '' + start
        count = 0
    # If data % 500000 == 0
    # Inserts remaining data
    if count > 0:
      query = query[:-1]
      query += end
      cursor.execute(query)
      db.commit()
    return len(data)

  # Returns the average statistics for a given topic
  def getState(self, topic):
    query = """SELECT AVG(p_words) AS p_words, AVG(n_words) AS n_words, 
      AVG(rating) AS rating, COUNT(*) AS tweet_count FROM tweets WHERE
      id IN (SELECT tweet_id FROM topics WHERE topic = %s);"""
    self.cursor.execute(query, (topic,))
    return self.cursor.fetchone()

  # Returns the number of tweets associated with a given topic
  def getCount(self, topic):
    self.cursor.execute('SELECT COUNT(*) AS count FROM topics WHERE topic = %s', (topic,))
    return self.cursor.fetchone()['count']

  # Returns the most common words associated with a given topic up to a given number of words
  def getWords(self, topic, limit):
    self.cursor.execute("""SELECT word, count FROM word_counts 
      WHERE topic = %s ORDER BY count DESC LIMIT %s;""", (topic, limit))
    return self.cursor.fetchall()

  # Returns the most common mentions associated with a given topic up to a given number of mentions
  def getMentions(self, topic, limit):
    self.cursor.execute("""SELECT mention, count FROM mentions
      WHERE topic = %s ORDER BY count DESC LIMIT %s;""", (topic, limit))
    return self.cursor.fetchall()

  # Returns the most common tags associated with a given topic up to a given number of tags
  def getTags(self, topic, limit):
    self.cursor.execute("""SELECT tag, count FROM tags
      WHERE topic = %s ORDER BY count DESC LIMIT %s;""", (topic, limit))
    return self.cursor.fetchall()