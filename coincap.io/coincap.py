import requests
import datetime
import sqlite3


conn = sqlite3.connect('btc@coincap.db')
db = conn.cursor()
db.execute('''
	create table if not exists btc
	(timestamp integer primary key,
	price integer)''')
response = requests.get('https://api.coincap.io/v2/assets/bitcoin/history?interval=m15').json()['data']
# response is a list with element like this:
#
# {'circulatingSupply': '18439037.0000000000000000', 'date': '2020-07-22T07:00:00.000Z', 'time': 1595401200000, 'priceUsd': '9358.5548389274721434'}
#
for i in range(0, len(response)):
	time = int(response[i]['time']/1000)
	price = int(float(response[i]['priceUsd']))
	db.execute("select * from btc where timestamp=:t", {"t": time})
	record = db.fetchone()
	if record is None:
		ts = datetime.datetime.fromtimestamp(time)
		print(ts.strftime('%Y-%m-%d %H:%M:%S'), price)
		db.execute("insert into btc(timestamp, price) values(?,?)",(time,price))
		conn.commit()
conn.close()
