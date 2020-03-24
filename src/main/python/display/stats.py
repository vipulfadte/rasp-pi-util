import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

RST = None

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding

x = 0

font = ImageFont.load_default()

while True:

    draw.rectangle((0,0,width,height), outline=0, fill=0)

    cmd = "hostname -I | cut -d\' \' -f1 | cut -d '.' -f4"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "iostat -cdx 1 2| awk 'NR==11 {printf \"%s%\",$3} NR==14 {printf \"|%s%\", $16} NR== 15 {printf \"|R: %.1fMb W: %.1fMb|%.0f%\", $4/125, $5/125, $16}'"
    details = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"MEM: %.2f/%.2fGB|%.0f%%\", $3/1024,$2/1024,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"SYSDSK: %d/%dGB\", $3,$2}'"
    Disk = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | grep sda1 | awk '/sda1/{printf \"NAS: %s/%sXB\", $3,$2}'|tr -d G|tr X G"
    Space = subprocess.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp | cut -d '=' -f2"
    Temp = subprocess.check_output(cmd, shell = True )

    dr = str(details).split('|');
    #CPU: 1.25%|MMCU: 0.00%|R: 0.0Mb W: 0.0Mb|Usg:0%

    draw.text((x, top),      "***STATS*** Node:" + str(IP), font=font, fill=255)
    draw.text((x, top+8),    "---------------------", font=font, fill=255)
    draw.text((x, top+15),   "CPU:" + dr[0] + "|" + str(Temp), font=font, fill=255)
    draw.text((x, top+25),   str(MemUsage),  font=font, fill=255)
    draw.text((x, top+35),   str(Disk) + "|" + dr[1],  font=font, fill=255)
    draw.text((x, top+45),   str(Space) + "|" + dr[3] , font=font, fill=255)
    draw.text((x, top+55),   dr[2], font=font, fill=255)

    disp.clear()
    disp.image(image)
    disp.display()
    time.sleep(.1)
