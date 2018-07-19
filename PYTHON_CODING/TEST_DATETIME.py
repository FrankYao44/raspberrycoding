import datetime
now=datetime.datetime.now()
print(now)
time=datetime.datetime(2000,2,29,7,31)
print(time)
print(time.timestamp())
c=1919191191.0
print(datetime.datetime.fromtimestamp(c))
c='2022-2-9 7:23:24'
n=datetime.datetime.strptime(c,'%Y-%m-%d %H:%M:%S' )
print(n)
print(n.strftime('%a, %m %d %H:%M'))
utc=datetime.timezone(datetime.timedelta(hours=8))
dt=now.replace(tzinfo=utc)
print(dt)
tokyo=dt.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
print(tokyo)
print(now+datetime.timedelta(weeks=3,days=3,hours=3))
