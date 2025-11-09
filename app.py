#!/bin/python3

import os
import sys
import time
import traceback
from flask import Flask, render_template, request
from threading import Thread
from src.power import power

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('start') == 'start':
            if power.get_power() == 1:
                # Already running
                pass
            elif power.get_power() == 2:
                # Resume from break without spawning a duplicate thread
                power.set_power(1)
            else:
                # Turn on and start laser in background thread
                power.set_power(1)
                from src.laser import Laser  # lazy import so app can run without RPi libs until needed
                laser = Laser([])
                try:
                    Thread(target=laser.run, daemon=True).start()
                except Exception as e:
                    print(e)
                    laser.turn_laser_off()
                    if type(e).__name__ != KeyboardInterrupt:
                        # Log error to file
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
        elif request.form.get('stop') == 'stop':
            power.set_power(0)
        else:
            # Update settings with robust parsing (handle '5.0' etc.)
            def parse_int(value, fallback):
                try:
                    if value is None:
                        return int(fallback)
                    return int(float(value))
                except Exception:
                    return int(fallback)

            current_speed = int(power.percentage_move_chance * 10)
            speed_val = parse_int(request.form.get('speed'), current_speed)
            delay_val = parse_int(request.form.get('delay'), power.delay_between_movements)
            points_val = parse_int(request.form.get('points'), power.num_points)

            if speed_val <= 0:
                power.set_percentage_move_chance(0)
            else:
                power.set_percentage_move_chance(speed_val/10)
            power.set_delay_between_movements(delay_val)
            power.set_num_points(points_val)
    return render_template('index.html',
                           speed=power.percentage_move_chance*10,
                           delay=power.delay_between_movements,
                           points=power.num_points)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
