import json
from string import punctuation
from __future__ import division

pos_file = open('text/positive.txt').read()
positive_words = pos_file.split('\n')

neg_file = open('text/negative.txt').read()
negative_words = pos_file.split('\n')

inv_file = open('text/invert.txt').read()
invert_words = pos_file.split('\n')

en_file = open('text/enhance.txt').read()
enhance_words = pos_file.split('\n')

def analysis(id, tag, tweet):

    out = {'tag': tag, 'id': id, 'text': tweet}
    neg = {}
    pos = {}
    positive_counter = 0
    negative_counter = 0

    t = tweet.lower()
    for p in list(punctuation):
        t.replace(p, '')

    words = t.split(' ')
    wc = len(words)

    multiplier = 1

    for word in words:
        if word != '':
            if word in positive_words:
                i = 1 * multiplier
                if word in pos:
                    pos[word] = pos[word] + i
                else:
                    pos[word] = i
                positive_counter = positive_counter + 1
                multiplier = 1
            elif word in negative_words:
                i = 1 * multiplier
                if word in neg:
                    neg[word] = neg[word] + i
                else:
                    neg[word] = neg[word] + i
                negative_counter = negative_counter + 1
                multiplier = 1
            elif word in invert_words:
                multiplier = multiplier * -1
            elif word in enhance_words:
                if multiplier > 0:
                    multiplier = multiplier + 1
                else:
                    multiplier = multiplier - 1
    res = positive_counter - negative_counter
    out['results'] = res
    out['positive_words'] = pos
    out['negative_words'] = neg
    out['p_count'] = positive_counter
    out['n_count'] = negative_counter
    out['word_count'] = wc
    out['rating'] = round((res/wc)*100, 2)
    return out
