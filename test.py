#!/usr/bin/env python
# -*- coding: utf-8 -*-
from string import punctuation
import datetime
import pymongo
import json
from textblob import TextBlob
import numpy as np
import sys
import re
from datetime import datetime, timedelta as td
import pandas as pd
from collections import Counter
import MySQLdb
import MyDB
import threading
from twython import Twython
import timeit
import matplotlib.pyplot as plt

'''
punc = list(punctuation)

t_str = 'Hello World!'

for p in punc:
  t_str = t_str.replace(p, '')

t_str = t_str.lower().replace(' ', '_')

print t_str


created_at = "Mon Oct 12 18:42:45 +0000 2009"

strp = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")

created_at = "Mon Oct 13 18:42:45 +0000 2009"

strp2 = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")

# tm_year
# tm_mon
# tm_mday
# tm_hour
# tm_min
# tm_sec
# tm_yday -- Year Day VIP

print strp < strp2


ids = [813135466971222026,81313546691522026]

client = pymongo.MongoClient('localhost', 27017)

db = client.test_db

posts = db.test_collection

test_array = [{"_id":1, "test": 12}, {"_id": 3, "test": 3.14}]

# Does no save document updates
try:
    posts.save(
        doc_or_docs=test_array,
        continue_on_error=True)
except pymongo.errors.DuplicateKeyError:
    pass

data = posts.find()

for p in data:
    print json.dumps(p)

t = {"a": "b"}
u = {"foo": "bar"}
x = t.copy()
t.update({"foo": "bar"})

print t

tweet = '@HeyTammyBruce @palin _posse Listening to Mr. Mittens speaking in PA. He reminds me of Reagan!'

blob = TextBlob(tweet)

polarity = []
subjectivity = []

for i in blob.sentences:
  polarity.append(i.sentiment.polarity)
  subjectivity.append(i.sentiment.subjectivity)

print np.mean(polarity)
print np.mean(subjectivity)


reload(sys)
sys.setdefaultencoding('utf8')


x = '[^A-Za-z0-9%s ]+' % punctuation

print x

tst = 'Final national NBC/WSJ poll before Tuesday: Obama 48 percent, Romney 47 ... - NBCNe...  ★ NTN:'
y = re.sub(x, '', tst)

print tst
print y

test1 = '2012-10-29'
test2 = '2012-11-05'

def dateRange(a, count):
  # Final end date
  d1 = datetime.strptime(a, "%Y-%m-%d").date()
  # count days prior
  d2 = d1 - td(days=count)
  delta = d1 - d2

  out = []

  # Create tuples, 1 day apart
  for i in range(delta.days + 1):
    db = d1 - td(days=i)
    da = db + td(days=1)
    out.append((db.strftime("%Y-%m-%d"), da.strftime("%Y-%m-%d")))
  return out

print dateRange(test2, 5)

df = pd.read_csv('data5/all.csv')

print 'Data Read'

print df.shape


print df.shape

df.to_csv('data5/test.csv')

i = ['data5/clinton.csv', 'data5/trump.csv']

print 'Test: %s' % i

test1 = {'a': 1, 'b': 2}
test2 = {'b': 3, 'c': 4}

print combine_dicts(test1, test2)


def combine_dicts(a, b):
  return dict(a.items() + b.items() +
    [(k, (a[k] + b[k])) for k in set(b) & set(a)])

test_data = open('data5/tmp/clinton.tmp', 'a+')
test_data.seek(0)
test = (test_data.read()).split('\n')

test.remove('')

test = map(json.loads, test)

out = {}

print test

def fileCompile(file):
  file.seek(0)
  data = (file.read()).split('\n')
  data.remove('')
  return map(json.loads, data)

def jsonMerge(file):
  rows = fileCompile(file)
  out = {}
  for row in rows:
    out = combine_dicts(out, row)
  return out

db = MyDB.MyDB()

test = 'oenonewept@noltenc@floridajayhawk'

t1 = test.split('@')

t2 = 'a'.split('@')

print t1, t2

def test(s):
  print 'Hello %s' % s

threads = []

for i in range(2):
  t = threading.Thread(target=test, args=(i,))
  threads.append(t)
  t.start()

for t in threads:
  t.join()

access_token = '787936570968043520-o1bHGOmR4AEuNoafsWoROAQIQIbwz3i'
access_token_secret = 's3vsnQAAuyLmhKYirZ0HIKRpreO8VsF84qAMDHfdmmmGG'
consumer_key = 'LJ0wq7eWPRSmdJVIoxQtYxyuy'
consumer_secret = 'CH811T3P1n7ofmPtd0POaML4vfGvKKIz7wLV212wKf3kRdp1i8'

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)


t = twitter.search(q='test', count=5)

with open('test.json', 'w+') as file:
  file.write(json.dumps(t, indent=2))

db = MyDB.MyDB()

print db.getWords('Mass Effect Andromeda', 10)

test1 = {}
test2 = []

for i in range(1000):
  string = 'test%s' % i
  test1[string] = 1
  test2.append(string)

def t1(string):
  try:
    return test1[string]
  except:
    return 0

def t2(string):
  if string in test2:
    return 1
  return 0

values = ['test1000','test99999','test500']

print timeit.timeit("[t1('test%s' % value) for value in range(5000)]", setup='from __main__ import t1', number=10000)
#36.0295689106
print timeit.timeit("[t2('test%s' % value) for value in range(5000)]", setup='from __main__ import t2', number=10000)
#436.308943987

out = {
}

pos_file = open('text/positive.txt').read()
positive_words = pos_file.split('\n')

neg_file = open('text/negative.txt').read()
negative_words = neg_file.split('\n')

for word in positive_words:
  out[word] = 1

for word in negative_words:
  out[word] = -1

with open('text/words.json', 'w+') as file:
  file.write(json.dumps(out, indent=2))

db = MyDB.MyDB()

db.reScan()
print range(1

def plotDates(Xs, Ys, topics, counts):
  l = len(Xs)
  if l == len(Ys) and len(Xs) == len(topics):
    title = ''
    for i in range(l):
      plt.plot(Xs[i], Ys[i], label=topics[i])
      title += '%s %s entries, ' % (counts[i], topics[i])
    title = title[:-2]
    plt.title(title)
    plt.xlabel('Time by hour')
    plt.ylabel('Average Rating')
    plt.legend(loc='best')
    plt.gcf().autofmt_xdate()
    print 'Displaying Graph. Close to continue'
    plt.show()
  else:
    print 'Inputs must be of equal length'

def toDF(data):
  out = []
  for row in data:
    out.append(row)
  return pd.DataFrame(out)

def toDate(dateString):
  try:
    return datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
  except TypeError:
    return dateString

db = MySQLdb.connect("localhost","wop","password","FYP" )
cursor = db.cursor(MySQLdb.cursors.DictCursor)

query = "SET sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'"

cursor.execute(query)

query = """SELECT date, rating FROM (
  SELECT t1.d2 AS date, AVG(rating * ((t1.retweets + 1)/t2.ar)) AS rating FROM
  (
    SELECT date AS d2, rating, retweets FROM tweets 
    WHERE id IN (SELECT tweet_id FROM topics WHERE topic = 'Mass Effect Andromeda')
  )AS t1 JOIN (
    SELECT date, AVG(retweets) AS ar FROM tweets
    WHERE id IN (SELECT tweet_id FROM topics WHERE topic = 'Mass Effect Andromeda')
    GROUP BY DATE(date), HOUR(date)
  ) AS t2 ON t1.d2 = t2.date
  GROUP BY DATE(t1.d2), HOUR(t1.d2)
) AS t
WHERE rating <> 0;"""

cursor.execute(query)
d = cursor.fetchall()

#print d

data = toDF(d)
data['date'] = data['date'].apply(toDate)

Xs = [data['date'].values]
Ys = [data['rating'].values]
topics = ['ME']
counts = [12]

print data

#plotDates(Xs, Ys, topics, counts)
'''

db = MyDB.MyDB()
y = db.getMentions('obama1', 10)
for x in y:
  print "%s & %s \\\\" % (x['mention'],x['count'])

print ''

y = db.getMentions('mccain', 10)
for x in y:
  print "%s & %s \\\\" % (x['mention'],x['count'])

print ''

y = db.getMentions('obama2', 10)
for x in y:
  print "%s & %s \\\\" % (x['mention'],x['count'])

print ''

y = db.getMentions('romney', 10)
for x in y:
  print "%s & %s \\\\" % (x['mention'],x['count'])

print ''

y = db.getMentions('trump', 10)
for x in y:
  print "%s & %s \\\\" % (x['mention'],x['count'])

print ''

y = db.getMentions('clinton', 10)
for x in y:
  print "%s & %s \\\\" % (x['mention'],x['count'])