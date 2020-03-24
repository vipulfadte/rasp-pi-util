import time
import os

import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

ON = True
RST = None

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def toggle(channel):
     global ON
     if ON:
	cmd = "ps -ef|grep -w  '/rasp-pi-util/src/main/python/display/stats.py' | awk 'NR==1 {printf \"%s\", $2}'"
    	process_id = subprocess.check_output(cmd, shell = True)
        os.system("kill -9 " + str(process_id))
        disp.begin()
    	disp.clear()
    	disp.display()
	ON = False
     else :
	os.system("python /rasp-pi-util/src/main/python/display/stats.py &")
    	ON =  True

GPIO.add_event_detect(16, GPIO.FALLING, callback = toggle, bouncetime = 2000)

while 1:
   time.sleep(1)
