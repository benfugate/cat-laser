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

### Setup (fresh install)

After cloning the repo on a Raspberry Pi, run the install script:

```bash
sudo bash install.sh
```

This will:
- Enable I2C (required for the servo controller)
- Install all Python dependencies
- Create the `errors/` log directory
- Install and enable the systemd service (auto-start on boot, running on port 80)

### Software (manual)

- Depends on Python 3
- Install pip packages: `pip install -r requirements.txt`

### Web UI
- Start the Flask app:
  - `python3 app.py`
- Open `http://<pi-ip>` (runs on port 80 by default; set `PORT` env var to override)
- Controls:
  - Start / Stop buttons
  - Sliders for Speed, Delay Between Movements, Number of Line Points
  - Timer settings: On Time, Sleep Min/Max
  - **Bounding Box**: Pan/Tilt min and max angles — changes save automatically and apply immediately to a running laser
  - All settings auto-save on change (no Apply button needed)

API:
- `GET /api/settings` → `{ speed, delay, points, on_time, sleep_min, sleep_max, power, status, on_remaining, break_remaining }`
- `POST /api/settings` with JSON subset to update immediately
- `GET /api/bounds` → `{ min_pan, max_pan, min_tilt, max_tilt }`
- `POST /api/bounds` with JSON subset to update and hot-reload into the running laser

### Diagnostics
- Servo sweep test:
  - `python3 src/servo_test.py`
- Interactive bounds (CLI alternative to the web UI):
  - `python3 set_bounds.py`
- Configuration (src/config.json):
  - `tilt_channel`, `pan_channel`
  - Optional: `*_pulse_min`, `*_pulse_max`

### Systemd service (recommended on Raspberry Pi)
- Example unit in `contrib/cat-laser.service`.
- Install/update:
  - `sudo cp contrib/cat-laser.service /etc/systemd/system/cat-laser.service`
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable cat-laser.service`
- Start/stop/restart/status:
  - `sudo systemctl start cat-laser.service`
  - `sudo systemctl stop cat-laser.service`
  - `sudo systemctl restart cat-laser.service`
  - `systemctl status cat-laser.service`
- Logs:
  - `journalctl -u cat-laser.service -f`
- Update and restart after pulling new code:
  - `cd /home/pi/cat-laser && git pull --ff-only && sudo systemctl restart cat-laser.service`

### CLI modes
> python3 src/laser.py

Exit with `CTRL-C`.

> python3 src/laser.py --manual

Enter pan,tilt values (e.g., `110,30`) and `q` to quit. This helps tune ranges.
