#!/usr/bin/env python3

import sys
import time
import random
import argparse
import numpy as np
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO


class ControlPower:
    """
    0 = off
    1 = on
    2 = paused for break
    """
    def __init__(self, power):
        self._power = power

    def get_power(self):
        return self._power

    def set_power(self, power):
        self._power = power
        print(f"Power set to {power.get_power()}")


class Laser:
    def __init__(self, args, power):
        """
        delay_between_movements: how often in seconds the laser will take a chance to move to a new location
        sleep_time_range: how many seconds (range) that the laser will sleep after running before starting automatically
        laser_on_time: how many seconds the laser will run when activated, before going to sleep
        percentage_move_chance: percentage chance that the laser will move
        pan_range: angle range that the pan servo will move between
        tilt_range: tilt range that the tilt servo will move between
        """
        # Settings
        self.power = power
        self.delay_between_movements = 1
        self.sleep_time_range = (1200, 5400)  # default: (1200, 5400)
        self.laser_on_time = 900  # default: 900
        self.counter = 0

        self.percentage_move_chance = 0.50
        self.pan_range = (50, 170)
        self.tilt_range = (30, 75)

        # Args
        parser = argparse.ArgumentParser(description="Automatic cat laser toy")
        parser.add_argument('--manual', action='store_true', help="manually enter values for movement to tune laser")
        self.tool_args, self.uk_args = parser.parse_known_args(args=args)

        # Internal values, change at own risk
        self.laser_off = 0
        self.laser_on = 1

        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, self.laser_on)
        time.sleep(1)

        kit = ServoKit(channels=16)
        self.tilt = kit.servo[0]
        self.pan = kit.servo[1]

        self.last_pan = 0
        self.last_tilt = 0

    def turn_laser_on(self):
        print("turning on")
        GPIO.output(17, self.laser_on)
        time.sleep(1)

    def turn_laser_off(self):
        print("turning off")
        GPIO.output(17, self.laser_off)
        time.sleep(1)

    def cleanup_for_quit(self):
        self.turn_laser_off()

    def create_laser_path(self, pan, tilt):
        pan_list = np.linspace(self.last_pan, pan, num=15)
        tilt_list = np.linspace(self.last_tilt, tilt, num=15)
        delay = random.uniform(0, 0.1)
        for index in range(len(pan_list)):
            self.move_laser(pan_list[index], tilt_list[index])
            self.counter += 1
            print(f"Moving... {self.counter}")
            time.sleep(delay)

    def move_laser(self, pan, tilt):
        self.tilt.angle = tilt
        self.pan.angle = pan
        self.last_pan = pan
        self.last_tilt = tilt
        time.sleep(0.03)  # give servos a chance to move

    def manual_control(self):
        print("enter 'q' to quit")
        userin = input("pan,tilt: ").split(",")
        while str(userin[0]).lower != "q":
            try:
                self.move_laser(int(userin[0]), int(userin[1]))
                userin = input("pan,tilt: ").split(",")
            except Exception as e:
                pass

    def pause_for_break(self, start_time):
        self.turn_laser_off()
        self.power.set_power = 2
        while time.time() < start_time:
            time.sleep(5)
            if self.power.get_power == 1:
                break
            if self.power.get_power == 0:
                return
        self.power.get_power = 1

    def run(self):
        if self.tool_args.manual:
            self.manual_control()
            return
        print(f"Movement chance:\n    {self.percentage_move_chance*100}% every {self.delay_between_movements} second")
        time.sleep(3)
        while True:
            self.turn_laser_on()
            on_time = time.time() + self.laser_on_time
            while time.time() < on_time:
                if random.random() < self.percentage_move_chance:
                    pan = random.randint(self.pan_range[0], self.pan_range[1])
                    tilt = random.randint(self.tilt_range[0], self.tilt_range[1])
                    self.create_laser_path(pan, tilt)
                time.sleep(self.delay_between_movements)
                if self.power.get_power == 0:
                    return
            print("taking a break")
            start_time = time.time() + random.randint(self.sleep_time_range[0], self.sleep_time_range[1])
            self.pause_for_break(start_time)


if __name__ == "__main__":
    laser = Laser(sys.argv[1:], ControlPower(1))
    laser.run()
