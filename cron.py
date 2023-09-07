import schedule
import time
from clear import clearDir

schedule.every(3).day.do(clearDir)

while True:
    schedule.run_pending()
    time.sleep(1)