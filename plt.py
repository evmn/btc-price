import datetime as dt
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

conn = sqlite3.connect('coincap.db')
db = conn.cursor()

db.execute("select timestamp from btc")
timestamp=db.fetchall()
time = [dt.datetime.fromtimestamp(t[0]) for t in timestamp]

db.execute("select price from btc")
price=db.fetchall()
conn.close()

x = time
y= [ p[0] for p in price]

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
