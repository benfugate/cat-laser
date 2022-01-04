#!/usr/bin/env python3
import os
import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, 1)
time.sleep(1)
GPIO.output(17, 0)

if os.path.isfile('/home/pi/cat-laser/src/active'):
    os.system("sudo -u root -S rm /home/pi/cat-laser/src/active")
if os.path.isfile('/home/pi/cat-laser/src/start-script'):
    os.system("sudo -u root -S rm /home/pi/cat-laser/src/start-script")
if os.path.isfile('/home/pi/cat-laser/src/stop-script'):
    os.system("sudo -u root -S rm /home/pi/cat-laser/src/stop-script")

print("Fixed!")
