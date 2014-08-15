import subprocess
import time

while True:
    subprocess.call('scrapy crawl war', shell=True)
    time.sleep(20)