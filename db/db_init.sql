CREATE TABLE tweets (id, text, p_count, n_count, w_count, retweets, date, time)

CREATE TABLE retweets (id, t_id, date, time)

CREATE TABLE p_words (t_id, word, count)

CREATE TABLE n_words (t_id, word, count)

CREATE TABLE topic (topic, t_id)
