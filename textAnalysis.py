#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import json
# !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
from string import punctuation
import re

# Import all functional words
inv_file = open('text/invert.txt').read()
invert_words = inv_file.split('\n')

en_file = open('text/enhance.txt').read()
enhance_words = en_file.split('\n')

boost_file = open('text/boost.txt').read()
boost_words = boost_file.split('\n')

dec_file = open('text/decrement.txt').read()
dec_words = dec_file.split('\n')

# Import positive and negative word dictionary
words = json.loads(open('text/words.json').read())

# Import emoji dictionary
emojis = json.loads(open('text/emojis.json').read())

# punctuation list without # and @
punc = list(punctuation.replace('#', '').replace('@', ''))

# Clear all unimportant punctuation from the string
def dePunc(word):
  for p in punc:
    word = word.replace(p, '')
  return word

# Text Analysis
def analysis(tweet):
  # If a tweet is somehow above a certain length ignore
  if len(tweet) > 300:
    return
  # Init output dictionary
  out = {'text': tweet}
  # Init counters
  positive_counter = 0
  negative_counter = 0
  # Init output dictionaries
  mentions = {}
  tags = {}
  word_count = {}
  # Set all text to lowercase to simplify analysis
  t = tweet.lower()
  # split by spaces
  tweet_words = t.split(' ')
  # Init word count and result
  wc = 0
  result = 0

  # Init multiplier
  multiplier = 1

  # Loop through words
  for word in tweet_words:
    # If word above 100 characters or below 5 characters ignore
    if len(word) < 100 and len(word) > 5:
      # increment word count
      wc += 1
      # Clear Punctuation except for @ and #
      # Record mentions and ignore for tone analysis
      if word[0] == '@':
        word = word[1:].replace("'", '')
        mentionString = word.split('@')
        word = dePunc(word)
        for mention in mentionString:
          try:
            mentions[mention] += 1
          except:
            mentions[mention] = 1
      else:
        # Double multiplier if hashtag and add to tags
        if word[0] == '#':
          multiplier *= 2
          word = word[1:]
          word = dePunc(word)
          try:
            tags[word] += 1
          except:
            tags[word] = 1
        # Clear special characters
        word = re.sub('[^A-Za-z0-9 ]+', '', dePunc(word))
        # Check if word in positive/negative words
        try:
          v = words[word]
        except:
          v = 0
        # Add to word Count
        try:
          word_count[word] += 1
        except:
          word_count[word] = 1
        # Prevent multiplying by 0
        if multiplier == 0:
          multiplier = 1
        # Word is positive
        if v > 0:
          i = v * multiplier
          # Increment count of postive words
          positive_counter += i
          # Reset multiplier
          multiplier = 1
        # If word is negative
        elif v < 0:
          i = v * multiplier
          # Increment count of negative words
          negative_counter += 1 * multiplier
          # Reset multiplier
          multiplier = 1
        # If word is inverter
        elif word in invert_words:
          multiplier = multiplier * -1
        # If word i high enhancement
        elif word in boost_words:
          multiplier *= 2
        # If word is light enchance
        elif word in enhance_words:
          if multiplier > 0:
            multiplier += 1
          else:
            multiplier -= 1
        # If word is light diminish
        elif word in dec_words:
          if multiplier > 0:
            multiplier += 1
          else:
            multiplier -= 1
        # Word in no categories/irrelevant
        else:
          # Reset multiplier
          multiplier = 1
    # If word is less than 5 character or more than 100
    else:
      try:
        result += emojis[word]
        # Include emojis in word count
        wc += 1
      except:
        pass

  # Total result
  result += (positive_counter - negative_counter)
  # Compile output dictionary
  out['results'] = result
  out['p_count'] = positive_counter
  out['n_count'] = negative_counter
  out['w_count'] = wc
  out['words'] = word_count
  out['mentions'] = mentions
  if wc != 0:
    out['rating'] = round((result/wc)*100, 2)
  else:
    out['rating'] = round(result, 2)
  out['tags'] = tags
  return out
