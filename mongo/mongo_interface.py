import pymongo
import json

client = pymongo.MongoClient('localhost', 27017)

db = client.test_db

posts = db.test_collection

'''
post = {
    "_id": 813135466971222026,
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"]
}

post_id = posts.insert_one(post).inserted_id
'''



data = posts.find_one({"_id": 813135466971222026})


#print json.dumps(data)


x = posts.find({"_id": 813135466971222026}, {"_id": 1}).count()

print x

def idExists(db_id):
    return bool(posts.find({"_id": db_id}).count())
