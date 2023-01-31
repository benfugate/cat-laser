#!/bin/python3

import os
import sys
import time
import traceback
from flask import Flask, render_template, request
from src.laser import Laser
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
                power.set_power(1)
            else:
                power.set_power(1)
                laser = Laser([])

                try:
                    laser.run()
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
        elif request.method == "POST":
            if int(request.form['speed']) == 0:
                power.set_percentage_move_chance(0)
            else:
                power.set_percentage_move_chance(int(request.form['speed'])/10)
            power.set_delay_between_movements(int(request.form['delay']))
            power.set_num_points(int(request.form['points']))
    return render_template('index.html',
                           speed=power.percentage_move_chance*10,
                           delay=power.delay_between_movements,
                           points=power.num_points)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
