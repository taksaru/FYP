import threading
import time
import twitterScraper
# Local imports
from MyDB import MyDB
import matplotlib.pyplot as plt
from datetime import datetime
import logging
import tweetHandler
import pandas as pd

# Initialise database and log
db = MyDB()

logging.basicConfig(filename='logs/queue_log.log',
  level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Placeholder to record max wait before all Threads can terminate safely
maxRate = 0

# Global boolean to control threads
running = True;

def getTweets(topic, rate, amount):
  # Wait before starting
  time.sleep(rate)
  while running:
    # Scrape tweets
    raw = twitterScraper.scrapeTweets(topic, amount)
    # If values returned
    if len(raw) > 0:
      # Log collected data
      logging.info('%s data Collected' % topic)
      # Run through handler
      tweets, words, mentions, tags = tweetHandler.handleTweets(raw, topic)
      logging.info('%s data Scanned' % topic)
      # Store analyzed tweets in database
      db.addTweets(tweets, words, mentions, tags)
      logging.info('%s data Recorded' % topic)
    else:
      logging.error('Scrape Error')
    # Log wait
    logging.info('Waiting %ss before attempting %s data collection' % (rate, topic))
    # Sleep until time for next request
    time.sleep(rate)
  # Log thread ending
  logging.info('%s Thread Dead' % topic)

employees = []

# create thread based on client dictionary
def makeClient(client):
  global maxRate
  if client['rate'] > maxRate:
    maxRate = client['rate']
  worker = threading.Thread(target=getTweets, args=(client['topic'], client['rate'], client['amount'],))
  employees.append(worker)
  worker.start()
  logging.info('%s Thread Started' % client['topic'])

# Add new client to database
def addClient():
  try:
    client = {}
    client['topic'] = raw_input('Enter Client Topic: ')
    client['rate'] = float(raw_input('Enter Client Request Rate: '))
    client['amount'] = int(raw_input('Enter Client Request Amount: '))
    db.storeClient(client)
    makeClient(client)
  except ValueError:
    print 'Invalid Input'

# Plots the average ratings of a given list of topics against the given dates
def plotDates(Xs, Ys, topics, counts):
  l = len(Xs)
  if l == len(Ys) and len(Xs) == len(topics):
    title = ''
    for i in range(l):
      plt.plot(Xs[i], Ys[i], label=topics[i])
      title += '%s %s entries, ' % (counts[i], topics[i])
    title = title[:-2]
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Average Rating')
    plt.legend(loc='best')
    plt.gcf().autofmt_xdate()
    print 'Displaying Graph. Close to continue'
    plt.show()
  else:
    print 'Inputs must be of equal length'

# Gets an input number from the Command Line User
def getInt(string):
  try:
    return int(raw_input(string))
  except:
    print 'Error: Input a Number'

# Requests before and after dates from the Command Line User
def getDates():
  before = validate(raw_input('Before Date[YYYY-MM-DD]: '))
  after = validate(raw_input('After Date[YYYY-MM-DD]: '))
  return before, after

# Attempts to convert a given string to a datetime, ignores empty strings but informs of incorrect formats
def validate(date_text):
  if date_text == '':
    return date_text
  try:
    datetime.strptime(date_text, '%Y-%m-%d')
    return date_text
  except ValueError:
    print "Incorrect data format, should be YYYY-MM-DD"
    return ''

# Instruction String for user
commands = """##############################
#                            #
#  ---INTERFACE COMMANDS---  #
#                            #
# * Add Client               #
# * Get Data                 #
# * ReScan                   #
# * View Data                #
# * Get State                #
# * Get Words                #
# * Get Mentions             #
# * Get Tags                 #
#                            #
# Available Topics:          #
# * Mass Effect Andromeda    #
# * obama1                   #
# * mccain                   #
# * palin                    #
# * obama2                   #
# * romney                   #
# * clinton                  #
# * trump                    #
#                            #
##############################"""

# Main Process
if __name__ == '__main__':
  # Create Client Threads
  for index, client in db.getClients().iterrows():
    makeClient(client)
  print 'Threads Built'
  try:
    while True:
      # Print instructions
      print commands
      keyIn = raw_input('Enter a Command: ')
      # Add client to database
      if keyIn == 'Add Client':
        print 'Adding Client'
        addClient()
      # Get all tweets associated with a given number of topics and save to file
      elif keyIn == 'Get Data':
        topicCount = getInt('Enter number of topics: ')
        if topicCount is not None:
          for i in range(topicCount):
            topic = raw_input('Enter Data Topic: ')
            location = raw_input('Enter Data Output Location: ')
            before, after = getDates()
            df = db.getData(topic, before, after)
            if len(df) == 0:
              print 'Data does not exist'
            else:
              try:
                df.to_csv(location, index=False)
                print 'Data stored at %s' % location
              except:
                print 'Location incompatible'
      # Updates Text Analysis without shutting down main and re-applies analysis to entire database without interrupting threads
      # All threads also benefit from updated analysis
      elif keyIn == 'ReScan':
        if raw_input('Are you sure? This could take alot of time. [y/n]: ') == 'y':
          logging.info('Beginning Total Database Rescan')
          start = time.time()
          dataLen = db.reScan()
          logging.info('Rescan of %s Tweets Complete' % dataLen)
          print 'Rescan Complete'
          taken = time.time()-start
          logging.info('Average Rescan took %ss' % (taken/dataLen))
        else:
          print 'Abandoning ReScan'
      # Graphs the average rating of a given number of topics over time grouping by hour or day
      elif keyIn == 'View Data':
        topicCount = getInt('Enter number of topics: ')
        if topicCount is not None:
          hour = False
          weight = False
          if raw_input('Hourly? [y/n]: ') == 'y':
            hour = True
          if raw_input('Weighted? [y/n]: ') == 'y':
            weight = True
          if topicCount > 0:
            topics = []
            Xs = []
            Ys = []
            counts = []
            befores = []
            afters = []
            for i in range(topicCount):
              topics.append(raw_input('Enter Data Topic: '))
              before, after = getDates()
              befores.append(before)
              afters.append(after)
            for i in range(topicCount):
              df = db.viewProgress(topics[i], hour, weight, befores[i], afters[i])
              counts.append(db.getCount(topics[i]))
              if df is None:
                print '%s Data does not exist' % topics[i]
                del topics[i]
                del befores[i]
                del afters[i]
              else:
                Xs.append(df['date'].values)
                Ys.append(df['rating'].values)
            if len(Xs) != 0:
              plotDates(Xs, Ys, topics, counts)
            else:
              print 'No Data to Graph'
          else:
            print 'Error: Invalid topic count'
      # Displays the average statistics for a given topic
      elif keyIn == 'Get State':
        topic = raw_input('Enter Data Topic: ')
        state = db.getState(topic)
        if state['tweet_count'] == 0:
          print 'No Data to Graph'
        else:
          print '----%s----' % topic
          print '%s Total Tweets' % state['tweet_count']
          print 'Average Rating: %s' % state['rating']
          print 'Average number of positive words: %s' % state['p_words']
          print 'Average number of negative words: %s' % state['n_words']
      # Displays the top words on a given topic
      elif keyIn == 'Get Words':
        topic = raw_input('Enter Data Topic: ')
        limit = getInt('Enter number of Entries: ')
        if limit is not None:
          words = db.getWords(topic, limit)
          if len(words) > 0:
            print '-----%s-----' % topic
            for word in words:
              print '%s:\t%s' % (word['word'], word['count'])
      # Displays the top mentions on a given topic
      elif keyIn == 'Get Mentions':
        topic = raw_input('Enter Data Topic: ')
        limit = getInt('Enter number of Entries: ')
        if limit is not None:
          mentions = db.getMentions(topic, limit)
          if len(mentions) > 0:
            print '-----%s-----' % topic
            for mention in mentions:
              print '%s:\t%s' % (mention['mention'], mention['count'])
      # Displays the top tags for a given topic
      elif keyIn == 'Get Tags':
        topic = raw_input('Enter Data Topic: ')
        limit = getInt('Enter number of Entries: ')
        if limit is not None:
          tags = db.getTags(topic, limit)
          if len(tags) > 0:
            print '-----%s-----' % topic
            for tag in tags:
              print '%s:\t%s' % (tag['tag'], tag['count'])
      # Begins terminating all Threads and terminates the script.
      elif keyIn == 'Shutdown':
        logging.info('Shutting Down')
        print 'Shutting Down'
        print 'Max time until Shutdown %s minutes' % (maxRate/60)
        running = False
        for i in employees:
          i.join()
        break
  except KeyboardInterrupt:
    print 'Shutting Down'
    running = False