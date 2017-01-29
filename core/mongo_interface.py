import pymongo
import json

client = pymongo.MongoClient('localhost', 27017)

db = client.test_db

def pull_topic(topic):
    collection = db.topics
    data = collection.find_one({"topic": topic})
    return data['tweets']

def pull_tweets(tweet_ids):
    collection = db.tweets
    return collection.find({"_id": {"$in": tweet_ids}})

def idExists(db_id):
    return bool(posts.find({"_id": db_id}).count())
