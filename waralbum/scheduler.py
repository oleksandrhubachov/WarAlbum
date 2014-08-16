import subprocess
import time

while True:
    subprocess.call('scrapy crawl war', shell=True)
    # time in seconds
    time.sleep(20)

    """
    Better to use cron in ubuntu
     sudo crontab -e
     add this to opened file
     0 */1 * * * cd /home/sashko/Documents/workspace/waralbum &&
                    scrapy crawl war &&
                    chown sashko. /home/sashko/Documents/workspace/waralbum/album
     Run
     sudo service cron restart
    """