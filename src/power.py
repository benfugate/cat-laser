class ControlPower:
    """
    0 = off
    1 = on
    2 = paused for break
    """
    def __init__(self, power_val):
        self._power = power_val
        self.delay_between_movements = 1
        self.percentage_move_chance = 0.50
        self.num_points = 15

    def set_delay_between_movements(self, delay):
        self.delay_between_movements = delay

    def set_percentage_move_chance(self, speed):
        self.percentage_move_chance = speed

    def set_num_points(self, num_points):
        self.num_points = num_points

    def get_power(self):
        return self._power

    def set_power(self, power_val):
        self._power = power_val
        print(f"Power set to {self.get_power()}")


power = ControlPower(0)
