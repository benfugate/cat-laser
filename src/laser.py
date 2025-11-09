#!/bin/python3

import os
import sys
import json
import time
import random
import argparse
import numpy as np
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
from src.power import power


class Laser:
    def __init__(self, args):
        """
        sleep_time_range: how many seconds (range) that the laser will sleep after running before starting automatically
        laser_on_time: how many seconds the laser will run when activated, before going to sleep
        pan_range: angle range that the pan servo will move between
        tilt_range: tilt range that the tilt servo will move between
        """
        # Settings
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/config.json") as f:
            config = json.load(f)
        self.sleep_time_range = config["sleep_time_range"]
        self.laser_on_time = config["laser_on_time"]
        self.pan_range = (config["min_pan"], config["max_pan"])
        self.tilt_range = (config["min_tilt"], config["max_tilt"])

        # Args
        parser = argparse.ArgumentParser(description="Automatic cat laser toy")
        parser.add_argument('--manual', action='store_true', help="manually enter values for movement to tune laser")
        self.tool_args, self.uk_args = parser.parse_known_args(args=args)

        # Internal values, change at own risk
        self.laser_off = 0
        self.laser_on = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, self.laser_on)
        time.sleep(1)

        kit = ServoKit(channels=16)
        tilt_channel = config.get("tilt_channel", 0)
        pan_channel = config.get("pan_channel", 1)
        self.tilt = kit.servo[tilt_channel]
        self.pan = kit.servo[pan_channel]
        # Optional per-servo calibration
        tmin, tmax = config.get("tilt_pulse_min"), config.get("tilt_pulse_max")
        pmin, pmax = config.get("pan_pulse_min"), config.get("pan_pulse_max")
        if tmin and tmax:
            try:
                self.tilt.set_pulse_width_range(int(tmin), int(tmax))
            except Exception:
                pass
        if pmin and pmax:
            try:
                self.pan.set_pulse_width_range(int(pmin), int(pmax))
            except Exception:
                pass

        self.last_pan = 0
        self.last_tilt = 0

        self.counter = 0

    def turn_laser_on(self):
        print("turning on")
        GPIO.output(17, self.laser_on)
        time.sleep(1)

    def turn_laser_off(self):
        print("turning off")
        GPIO.output(17, self.laser_off)
        time.sleep(1)

    def create_laser_path(self, pan, tilt):
        pan_list = np.linspace(self.last_pan, pan, num=power.num_points)
        tilt_list = np.linspace(self.last_tilt, tilt, num=power.num_points)
        delay = random.uniform(0, 0.1)
        for index in range(len(pan_list)):
            self.move_laser(pan_list[index], tilt_list[index])
            self.counter += 1
            print(f"Moving... {self.counter}")
            time.sleep(delay)

    def move_laser(self, pan, tilt):
        # Clamp and coerce to valid range and int to avoid out-of-range errors
        try:
            pan = int(round(float(pan)))
            tilt = int(round(float(tilt)))
        except Exception:
            # Fallback if conversion fails
            pan = 90
            tilt = 90
        pan = max(0, min(180, pan))
        tilt = max(0, min(180, tilt))

        self.tilt.angle = tilt
        self.pan.angle = pan
        self.last_pan = pan
        self.last_tilt = tilt
        time.sleep(0.03)  # give servos a chance to move

    def manual_control(self):
        print("enter 'q' to quit")
        while True:
            try:
                userin = input("pan,tilt: ")
                if userin.strip().lower() == 'q':
                    break
                pan_str, tilt_str = userin.split(",")
                self.move_laser(int(pan_str), int(tilt_str))
            except ValueError:
                print("Invalid input. Use format: pan,tilt or 'q' to quit")
            except Exception as e:
                print(f"Error: {e}")

    def pause_for_break(self, start_time):
        self.turn_laser_off()
        power.set_power(2)
        while time.time() < start_time:
            time.sleep(5)
            if power.get_power() == 1:
                break
            if power.get_power() == 0:
                return
        power.set_power(1)

    def run(self):
        if self.tool_args.manual:
            self.manual_control()
            return
        print(f"Movement chance:\n    {power.percentage_move_chance*100}% every {power.delay_between_movements} second")
        time.sleep(3)
        while True:
            self.turn_laser_on()
            on_time = time.time() + self.laser_on_time
            while time.time() < on_time:
                if random.random() < power.percentage_move_chance:
                    pan = random.randint(self.pan_range[0], self.pan_range[1])
                    tilt = random.randint(self.tilt_range[0], self.tilt_range[1])
                    self.create_laser_path(pan, tilt)
                time.sleep(power.delay_between_movements)
                if power.get_power() == 0:
                    self.turn_laser_off()
                    try:
                        GPIO.cleanup()
                    except Exception:
                        pass
                    return
            print("taking a break")
            start_time = time.time() + random.randint(self.sleep_time_range[0], self.sleep_time_range[1])
            self.pause_for_break(start_time)


if __name__ == "__main__":
    laser = Laser(sys.argv[1:])
    laser.run()
