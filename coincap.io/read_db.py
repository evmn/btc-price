import datetime
import sqlite3

conn = sqlite3.connect('btc@coincap.db')
db = conn.cursor()

db.execute("select timestamp,price from btc")
data=db.fetchall()
for time,price in data:
	t = datetime.datetime.fromtimestamp(time)
	print(t.strftime('%Y-%m-%d %H:%M:%S,'), price)

conn.close()
