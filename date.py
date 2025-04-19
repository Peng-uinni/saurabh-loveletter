import datetime


print(datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S"))
print(datetime.datetime.now(datetime.timezone.utc).date())
print(datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S  %z"))