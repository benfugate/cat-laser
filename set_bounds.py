#!/bin/python3

import json
import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO


class SetBounds:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, 1)
        time.sleep(1)

        with open("src/config.json") as f:
            self.config = json.load(f)
        kit = ServoKit(channels=16)
        self.tilt = kit.servo[0]
        self.pan = kit.servo[1]
        self.move_laser(110, self.config["min_tilt"])

    def move_laser(self, pan, tilt):
        try:
            self.pan.angle = pan
            self.tilt.angle = tilt
            time.sleep(0.03)  # give servos a chance to move
        except ValueError:
            print("[ERROR] Laser angle defined beyond the possible angle, go back to a valid value")

    def set_bound_value(self, bound_option, entry):
        if entry == "+":
            self.config[bound_option] += 1
        elif entry == "++":
            self.config[bound_option] += 10
        elif entry == "-":
            self.config[bound_option] -= 1
        elif entry == "--":
            self.config[bound_option] -= 10

    def execute(self):
        print("-- Setting laser bounds --")

        for bound_option in ["min_tilt", "max_tilt", "min_pan", "max_pan"]:
            # Show current bound value
            if "tilt" in bound_option:
                self.move_laser(110, self.config[bound_option])
            elif "pan" in bound_option:
                tilt_middle = (self.config["min_tilt"] + self.config["max_tilt"]) / 2
                self.move_laser(self.config[bound_option], tilt_middle)

            print(f"Setting {bound_option} value. Current value: {self.config[bound_option]}")
            print("Options:\n\t+ = increase\n\t- = decrease\n\t++ = increase 10\n\t-- = decrease 10\n\ta = accept")
            entry = input("Enter a value (+/-/++/--/a): ")
            while entry != "a":
                self.set_bound_value(bound_option, entry)
                if "tilt" in bound_option:
                    self.move_laser(110, self.config[bound_option])
                elif "pan" in bound_option:
                    tilt_middle = (self.config["min_tilt"] + self.config["max_tilt"]) / 2
                    self.move_laser(self.config[bound_option], tilt_middle)
                entry = input("Enter a value (+/-/++/--/a): ")

            print(f"{bound_option} set to {self.config[bound_option]}")
            with open("src/config.json", "w") as f:
                json.dump(self.config, f, indent=2)

        # Save and exit
        GPIO.output(17, 0)
        try:
            GPIO.cleanup()
        except Exception:
            pass
        print("Done!")


if __name__ == '__main__':
    bounds = SetBounds()
    bounds.execute()
