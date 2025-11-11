class ControlPower:
    """
    0 = off
    1 = on
    2 = paused for break
    """
    def __init__(self, power_val):
        self._power = power_val
        # Movement behavior
        self.delay_between_movements = 1
        self.percentage_move_chance = 0.50
        self.num_points = 15
        # Timer behavior
        self.laser_on_time = 900  # seconds
        self.sleep_min = 1200     # seconds
        self.sleep_max = 5400     # seconds
        # Runtime state for UI countdowns (epoch seconds)
        self.on_until = None
        self.break_until = None

    # Movement setters
    def set_delay_between_movements(self, delay):
        self.delay_between_movements = int(delay)

    def set_percentage_move_chance(self, speed):
        self.percentage_move_chance = float(speed)

    def set_num_points(self, num_points):
        self.num_points = int(num_points)

    # Timer setters
    def set_laser_on_time(self, seconds):
        self.laser_on_time = int(seconds)

    def set_sleep_range(self, sleep_min, sleep_max):
        self.sleep_min = int(sleep_min)
        self.sleep_max = int(sleep_max)

    # Power state
    def get_power(self):
        return self._power

    def set_power(self, power_val):
        self._power = power_val
        print(f"Power set to {self.get_power()}")


power = ControlPower(0)
