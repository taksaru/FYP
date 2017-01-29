from string import punctuation
import datetime
import pymongo
import json

'''
punc = list(punctuation)

t_str = 'Hello World!'

for p in punc:
  t_str = t_str.replace(p, '')

t_str = t_str.lower().replace(' ', '_')

print t_str


created_at = "Mon Oct 12 18:42:45 +0000 2009"

strp = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")

created_at = "Mon Oct 13 18:42:45 +0000 2009"

strp2 = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")

# tm_year
# tm_mon
# tm_mday
# tm_hour
# tm_min
# tm_sec
# tm_yday -- Year Day VIP

print strp < strp2
'''

ids = [813135466971222026,81313546691522026]

client = pymongo.MongoClient('localhost', 27017)

db = client.test_db

posts = db.test_collection

test_array = [{"_id":1, "test": 12}, {"_id": 3, "test": 3.14}]

# Does no save document updates
try:
    posts.save(
        doc_or_docs=test_array,
        continue_on_error=True)
except pymongo.errors.DuplicateKeyError:
    pass

data = posts.find()

for p in data:
    print json.dumps(p)
'''

t = {"a": "b"}
u = {"foo": "bar"}
x = t.copy()
t.update({"foo": "bar"})

print t
'''
