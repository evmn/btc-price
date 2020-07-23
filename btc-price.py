import requests
import datetime
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

coincap_api='https://api.coincap.io/v2/assets/bitcoin/history?interval=m1'

conn = sqlite3.connect('coincap.db')
db = conn.cursor()
db.execute("create table if not exists btc(timestamp integer primary key, price integer)")
response = requests.get(coincap_api).json()['data']

# response is a list, with elements like:
#
# {
#	'circulatingSupply': '18439037.0000000000000000',
#	'date': '2020-07-22T07:00:00.000Z',
#	'time': 1595401200000, 
#	'priceUsd': '9358.5548389274721434'
# }
#
x = []
y = []

for i in range(0, len(response)):
	time = int(response[i]['time']/1000)
	price = int(float(response[i]['priceUsd']))
	
	dt = datetime.datetime.fromtimestamp(time)
	x.append(dt)
	y.append(price)

	db.execute("select * from btc where timestamp=:t", {"t": time})
	record = db.fetchone()
	if record is None:
		print(i, dt.strftime(', %Y-%m-%d %H:%M:%S, '), price)
		db.execute("insert into btc(timestamp, price) values(?,?)",(time,price))

conn.commit()
conn.close()

fig, ax = plt.subplots()
#fmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
fmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(fmt)

hour = mdates.HourLocator(interval=2)
minute = mdates.MinuteLocator(interval=30)
ax.xaxis.set_major_locator(hour)
ax.xaxis.set_minor_locator(minute)

ax.grid(True)
ax.set_title("BTC Price in Last 24 Hours")
ax.plot(x,y)
fig.autofmt_xdate()
plt.show()
