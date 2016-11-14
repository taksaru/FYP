/* STANDARD INSERTION (assuming no duplicates) */
INSERT INTO tweets VALUES (o['id'], o['text'], o['p_count'], o['n_count'], o['w_count'], 0, decoded_date, decoded_time)
INSERT INTO p_words VALUES (o['id'], o['positive_words'][word], o['positive_words'][count])
INSERT INTO n_words VALUES (o['id'], o['negative_words'][word], o['negative_words'][count])
INSERT INTO topic VALUES (o['tag'], p['id'])

/* IF RETWEET */
INSERT INTO retweets VALUES (rt_id, og_id, decoded_date, decoded_time)
UPDATE tweets SET retweets = retweets + 1 WHERE id = og_id
