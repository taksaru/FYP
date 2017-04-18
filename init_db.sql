DROP TABLE IF EXISTS tweets, topics, word_counts, mentions, tags, clients;

CREATE TABLE tweets (
  id VARCHAR(20) PRIMARY KEY,
  text VARCHAR(200),
  p_words SMALLINT,
  n_words SMALLINT,
  rating FLOAT,
  username VARCHAR(25),
  retweets INT,
  date TIMESTAMP
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
  topic VARCHAR(25)
  tag VARCHAR(255),
  count INT,
  PRIMARY KEY (topic, tag)
);

CREATE TABLE clients (
  topic VARCHAR(25) PRIMARY KEY,
  rate INT,
  amount INT
);
