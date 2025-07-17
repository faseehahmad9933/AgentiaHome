import datetime
import time

now = datetime.datetime.now()
wait_time = datetime.timedelta(seconds=20)
future_time = now + wait_time

print(f"Waiting for 20 seconds, starting at {now}")

time.sleep(wait_time.total_seconds())

print(f"Waited for 20 seconds. Current time: {datetime.datetime.now()}")