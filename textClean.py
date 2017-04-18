#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from string import punctuation
import sys

reload(sys)
sys.setdefaultencoding('utf8')

library = '[^A-Za-z0-9%s ]+' % punctuation

# Remove surrounding quotes from a string
def deQuote(txt):
  if txt.startswith('"') and txt.endswith('"') or txt.startswith("'") and txt.endswith("'"):
    txt = txt[1:-1]
  return txt

# Remove link from a string (Not 100% Effective)
def deLink(txt):
  before = len(txt)
  if 'https://' in txt:
    txt = txt.replace('https://www. ', 'http://')
    txt = re.sub(r"http\S+", "…", txt)
    txt = re.sub('….*?…', '', txt)
  elif 'http://' in txt:
    txt = txt.replace('http:// ', 'http://')
    txt = re.sub(r"http\S+", "", txt)
  words = txt.split(' ')
  txt = ''
  for word in words:
    if (len(word) > 5 and len(word) < 100):
      txt += word + ' '
  after = len(txt)
  if after < (before/2):
    return ''
  return txt

# Attempts to clean string
def clean(txt):
  txt = deLink(deQuote(txt))
  txt = re.sub(library, '', txt)
  return txt
