#!/bin/python3

import time
import json
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO


def load_config():
    with open("src/config.json") as f:
        return json.load(f)


def setup_servos(cfg):
    kit = ServoKit(channels=16)
    tilt_ch = cfg.get("tilt_channel", 0)
    pan_ch = cfg.get("pan_channel", 1)
    tilt = kit.servo[tilt_ch]
    pan = kit.servo[pan_ch]

    tmin, tmax = cfg.get("tilt_pulse_min"), cfg.get("tilt_pulse_max")
    pmin, pmax = cfg.get("pan_pulse_min"), cfg.get("pan_pulse_max")
    if tmin and tmax:
        tilt.set_pulse_width_range(tmin, tmax)
    if pmin and pmax:
        pan.set_pulse_width_range(pmin, pmax)
    return pan, tilt, pan_ch, tilt_ch


def main():
    cfg = load_config()

    print("-- Servo Diagnostic --")
    print("Using channels -> pan:{}, tilt:{}".format(cfg.get("pan_channel", 1), cfg.get("tilt_channel", 0)))

    GPIO.setmode(GPIO.BCM)
    try:
        pan, tilt, pan_ch, tilt_ch = setup_servos(cfg)

        mid_pan = int((cfg["min_pan"] + cfg["max_pan"]) / 2)
        mid_tilt = int((cfg["min_tilt"] + cfg["max_tilt"]) / 2)

        # Center both
        print("Centering both servos...")
        pan.angle = mid_pan
        tilt.angle = mid_tilt
        time.sleep(1)

        # Test tilt sweep
        print("Sweeping TILT on channel {} from min to max".format(tilt_ch))
        for a in [cfg["min_tilt"], mid_tilt, cfg["max_tilt"], mid_tilt]:
            tilt.angle = int(a)
            print("Tilt ->", a)
            time.sleep(0.8)

        # Test pan sweep
        print("Sweeping PAN on channel {} from min to max".format(pan_ch))
        for a in [cfg["min_pan"], mid_pan, cfg["max_pan"], mid_pan]:
            pan.angle = int(a)
            print("Pan ->", a)
            time.sleep(0.8)

        print("If the wrong axis moves, swap pan_channel and tilt_channel in src/config.json and re-run.")
    finally:
        try:
            GPIO.cleanup()
        except Exception:
            pass


if __name__ == "__main__":
    main()
