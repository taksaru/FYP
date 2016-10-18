import sqlite3
import json

c = sqlite3.connect("test.db")

c.execute("CREATE TABLE positive (id, word)")

c.execute("INSERT INTO positive VALUES (1, 'good')")

c.commit()

for row in c.execute("SELECT * FROM positive"):
    print json.dumps(row)
