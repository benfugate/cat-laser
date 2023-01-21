class ControlPower:
    """
    0 = off
    1 = on
    2 = paused for break
    """
    def __init__(self, power_val):
        self._power = power_val

    def get_power(self):
        return self._power

    def set_power(self, power_val):
        self._power = power_val
        print(f"Power set to {self.get_power()}")


power = ControlPower(0)
