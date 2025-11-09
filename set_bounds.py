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
        tilt_channel = self.config.get("tilt_channel", 0)
        pan_channel = self.config.get("pan_channel", 1)
        print(f"Using channels -> pan:{pan_channel}, tilt:{tilt_channel}")
        self.tilt = kit.servo[tilt_channel]
        self.pan = kit.servo[pan_channel]
        # Optional per-servo calibration
        tmin, tmax = self.config.get("tilt_pulse_min"), self.config.get("tilt_pulse_max")
        pmin, pmax = self.config.get("pan_pulse_min"), self.config.get("pan_pulse_max")
        try:
            if tmin and tmax:
                self.tilt.set_pulse_width_range(int(tmin), int(tmax))
        except Exception:
            pass
        try:
            if pmin and pmax:
                self.pan.set_pulse_width_range(int(pmin), int(pmax))
        except Exception:
            pass
        # Move to a safe starting position
        tilt_middle = (self.config["min_tilt"] + self.config["max_tilt"]) / 2
        self.move_laser(110, tilt_middle)

    def move_laser(self, pan, tilt):
        try:
            print(f"[DEBUG] move_laser: pan={pan}, tilt={tilt}")
            self.pan.angle = pan
            self.tilt.angle = tilt
            time.sleep(0.2)  # give servos a chance to move
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
