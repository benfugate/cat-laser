import os
import time
import random
import numpy as np
from adafruit_servokit import ServoKit


class Laser:
    def __init__(self):
        """
        move_delay_seconds: how often in seconds the laser will take a chance to move to a new location
        percentage_move_chance: percentage chance that the laser will move
        pan_range: angle range that the pan servo will move between
        tilt_range: tilt range that the tilt servo will move between
        """
        self.move_delay_seconds = 1
        self.percentage_move_chance = 0.50
        self.pan_range = (0, 120)
        self.tilt_range = (80, 130)

        self.last_pan = 0
        self.last_tilt = 0

        kit = ServoKit(channels=16)
        self.tilt = kit.servo[0]
        self.pan = kit.servo[1]

    def create_laser_path(self, pan, tilt):
        pan_list = np.linspace(self.last_pan, pan, num=30)
        tilt_list = np.linspace(self.last_tilt, tilt, num=30)
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
        print(f"Movement chance:\n    {self.percentage_move_chance*100}% every {self.move_delay_seconds} second")
        while True:
            on_time = time.time() + 900
            while time.time() < on_time:
                if os.path.isfile('/home/pi/cat-laser/src/start-script'):
                    os.system("sudo -u root -S rm /home/pi/cat-laser/src/start-script")
                if random.random() < self.percentage_move_chance:
                    pan = random.randint(self.pan_range[0], self.pan_range[1])
                    tilt = random.randint(self.tilt_range[0], self.tilt_range[1])
                    self.create_laser_path(pan, tilt)
                time.sleep(self.move_delay_seconds)
                if os.path.isfile('/home/pi/cat-laser/src/stop-script'):
                    return
            laser.tilt.angle = 11.5
            laser.pan.angle = 110
            start_time = time.time() + random.randint(1200, 5400)
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
        laser.run()
        os.system("sudo -u root -S rm /home/pi/cat-laser/src/active")
    else:
        exit(0)
except KeyboardInterrupt:
    print("Goodbye!")

"""
These tilt and pan angles put the laser in a place that my cat cant see it, so when I stop
the toy the laser is out of the way. When I get a 5v relay, Ill turn off the laser instead.
"""
laser.tilt.angle = 11.5
laser.pan.angle = 110
if os.path.isfile('/home/pi/cat-laser/src/stop-script'):
    os.system("sudo -u root -S rm /home/pi/cat-laser/src/stop-script")
