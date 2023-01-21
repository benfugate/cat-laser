# Random Cat Laser Toy

I bought an automatic cat laser pointer toy on Amazon, but my cat quickly got bored
with it likely due to its predictability of just going in circles. I decided to make
one myself with a Raspberry Pi Zero I had lying around.

Essentially, this tool will move the laser to a random point in a square grid using
a couple servos to get a PTZ effect. I have it hanging from my ceiling in my living
room, but it can really be set up anywhere.

The PTZ servos and the laser are both 5v and get fed from the Pi, so everything
operates on one USB power cable.

### Hardware

You can really get this stuff wherever this is just what I got

- Raspberry Pi <em>[(adafruit)](https://www.adafruit.com/product/3708) </em>
  - Any Pi with gpio headers should be fine. I am using a Zero 2 W with GPIO pins I soldered
- Servos <em>[(Amazon)](https://smile.amazon.com/gp/product/B08PK9N9T4) </em>
- Lasers <em>[(Amazon)](https://smile.amazon.com/dp/B071FT9HSV/) </em>
- 5v Relays <em>[(Amazon)](https://smile.amazon.com/gp/product/B00LW15A4W/) </em>


I 3D printed a case that houses the Pi and the relay, and the servos are mounted on top of it.
I may post these files once I refine it a bit.

### Software

- Depends on Python 3
- Run `pip install -r requirements.txt` to install required pip packages
- Open <b>laser.py</b> and change the following variables to suit your own needs.
There is a small help note outlining the purpose of each variable in the file.
  - `move_delay_seconds`
  - `percentage_move_chance`
  - `pan_range`
  - `tilt_range`

### Usage
> python3 src/laser.py

Exit the program with `CTRL-C`

When exited, the program will move the laser to a specified hardcoded location
specified at the bottom of laser.py. This can be modified to suit your own needs.

> python3 src/laser.py --manual

Running in this mode will allow the user to input a "pan, tilt" value to see where the laser will land.
This should help the user tune where the laser should land in their own space.
