#!/usr/bin/env python3
import os
import sys
import time
import random
import numpy as np
import traceback
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO

class Laser:
    def __init__(self):
        """
        delay_between_movements: how often in seconds the laser will take a chance to move to a new location
        sleep_time_range: how many seconds (range) that the laser will sleep after running before starting automatically
        laser_on_time: how many seconds the laser will run when activated, before going to sleep
        percentage_move_chance: percentage chance that the laser will move
        pan_range: angle range that the pan servo will move between
        tilt_range: tilt range that the tilt servo will move between
        """
        self.delay_between_movements = 0
        #self.sleep_time_range = (1200, 5400)
        self.sleep_time_range = (5, 10)
        self.laser_on_time = 5

        self.percentage_move_chance = 0.50
        self.pan_range = (0, 120)
        self.tilt_range = (80, 130)

        self.last_pan = 0
        self.last_tilt = 0

        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, 1)
        time.sleep(1)
        GPIO.output(17, 0)

        self.laser_off = 0
        self.laser_on = 1

        kit = ServoKit(channels=16)
        self.tilt = kit.servo[0]
        self.pan = kit.servo[1]

    def create_laser_path(self, pan, tilt):
        pan_list = np.linspace(self.last_pan, pan, num=15)
        tilt_list = np.linspace(self.last_tilt, tilt, num=15)
        delay = random.uniform(0, 0.1)
        for index in range(len(pan_list)):
            self.move_laser(pan_list[index], tilt_list[index])
            time.sleep(delay)

    def move_laser(self, pan, tilt):
        self.tilt.angle = tilt
        self.pan.angle = pan
        self.last_pan = pan
        self.last_tilt = tilt
        time.sleep(0.03)  # give servos a chance to move

    def run(self):
        print(f"Movement chance:\n    {self.percentage_move_chance*100}% every {self.delay_between_movements} second")
        time.sleep(3)
        while True:
            GPIO.output(17, self.laser_on)
            print("turning on")
            on_time = time.time() + 900
            while time.time() < on_time:
                if os.path.isfile('/home/pi/cat-laser/src/start-script'):
                    os.system("sudo -u root -S rm /home/pi/cat-laser/src/start-script")
                if random.random() < self.percentage_move_chance:
                    pan = random.randint(self.pan_range[0], self.pan_range[1])
                    tilt = random.randint(self.tilt_range[0], self.tilt_range[1])
                    self.create_laser_path(pan, tilt)
                time.sleep(self.delay_between_movements)
                if os.path.isfile('/home/pi/cat-laser/src/stop-script'):
                    return
            GPIO.output(17, self.laser_off)
            print("turning off for a break")
            start_time = time.time() + random.randint(self.sleep_time_range[0], self.sleep_time_range[1])
            while time.time() < start_time:
                time.sleep(5)
                if os.path.isfile('/home/pi/cat-laser/src/start-script'):
                    break
            if os.path.isfile('/home/pi/cat-laser/src/stop-script'):
                return


laser = Laser()
try:
    if not os.path.isfile('/home/pi/cat-laser/src/active'):
        os.system("sudo -u root -S touch /home/pi/cat-laser/src/active")
        try:
            laser.run()
        except Exception as e:
            if os.path.isfile('/home/pi/cat-laser/src/active'):
                os.system("sudo -u root -S rm /home/pi/cat-laser/src/active")
            if os.path.isfile('/home/pi/cat-laser/src/start-script'):
                os.system("sudo -u root -S rm /home/pi/cat-laser/src/start-script")
            if os.path.isfile('/home/pi/cat-laser/src/stop-script'):
                os.system("sudo -u root -S rm /home/pi/cat-laser/src/stop-script")
            GPIO.output(17, laser.laser_off)
    else:
        errors_dir = f'{os.getcwd()}/errors/'
        if not os.path.exists(errors_dir):
            os.makedirs(errors_dir)

        list_of_files = os.listdir(errors_dir)
        full_path = ["{0}/{1}".format(errors_dir, x) for x in list_of_files]
        if len(list_of_files) == 5:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)
        with open(f"{errors_dir}/exception-{int(time.time())}.txt", "w") as errorfile:
            e_type, e_val, e_tb = sys.exc_info()
            traceback.print_exception(e_type, e_val, e_tb, file=errorfile)
except KeyboardInterrupt:
    os.system("sudo -u root -S rm /home/pi/cat-laser/src/active")
    print("Goodbye!")

GPIO.output(17, laser.laser_off)
print("laser off, done")
if os.path.isfile('/home/pi/cat-laser/src/active'):
    os.system("sudo -u root -S rm /home/pi/cat-laser/src/active")
if os.path.isfile('/home/pi/cat-laser/src/start-script'):
    os.system("sudo -u root -S rm /home/pi/cat-laser/src/start-script")
if os.path.isfile('/home/pi/cat-laser/src/stop-script'):
    os.system("sudo -u root -S rm /home/pi/cat-laser/src/stop-script")
