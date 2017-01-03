import text_analysis
import json

tweets = open("text/obama.txt").read()
tweet_list = tweets.split('\n')

o = []

for i in tweet_list:
    o.append(text_analysis.analysis(123, 'obama', i))

with open('test.json', 'w') as f:
    f.write(json.dumps(o))

tweets_insert = 'INSERT INTO tweets VALUES '
p_words_insert = 'INSERT INTO p_words VALUES '
n_words_insert = 'INSERT INTO n_words VALUES '
topic_insert = 'INSERT INTO topic VALUES '

for i in o:
    tweets_insert = tweets_insert + '(' + str(i['id']) + ', ' + str(i['text']) + ', ' + str(i['p_count']) + ', ' + str(i['n_count']) + ', ' + str(i['w_count']) + ', 0, date, time),'
    for key, value in i['positive_words'].items():
        p_words_insert = p_words_insert + '(' + str(i['id']) + ', ' + str(key) + ', ' + str(value) + '),'
    for key, value in i['negative_words'].items():
        n_words_insert = n_words_insert + '(' + str(i['id']) + ', ' + str(key) + ', ' + str(value) + '),'
    topic_insert = topic_insert + '(' + str(i['id']) + ', ' + str(i['tag']) + '),'

tweets_insert = tweets_insert[:-1]
p_words_insert = p_words_insert[:-1]
n_words_insert = n_words_insert[:-1]
topic_insert = topic_insert[:-1]

with open('test.txt', 'w') as f:
    f.write(tweets_insert)
    f.write('\n')
    f.write(p_words_insert)
    f.write('\n')
    f.write(n_words_insert)
    f.write('\n')
    f.write(topic_insert)
