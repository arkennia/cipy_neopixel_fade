# (c) Jonathan Manly 2022-
# This source code is licensed under the MIT license.
# See LICENSE for details.

"""
A library for CircuitPython that creates a fade animation using Neopixels.

Reqires:
`adafruit_ticks`
"""
import adafruit_ticks

__INCREASING = 0
__HOLDING_LOW = 1
__HOLDING_HIGH = 2
__DECREASING = 3


class Fade:
    """Creates a fading, or pulsing animation on a single channel."""

    def __init__(self, bright_hold_t, dim_hold_t, bright_t, dim_t, max_val, min_val):
        """
        Intialize the Fade class.
        Keyword Arguments:
            bright_hold_t: Number of ticks to hold at the max setting.
            dim_hold_t: Number of ticks to hold at min setting.
            bright_t: The amount of ticks to get to max setting.
            dim_t the amount of ticks to get to min setting.
            max_val: The maximum brightness, typically 0-255.
            min_val: The minimum brightness, typically 0-255.
        """
        self._bright_hold_t = bright_hold_t
        self._bright_t = bright_t
        self._dim_t = dim_t
        self._dim_hold_t = dim_hold_t
        self._max_val = max_val
        self._min_val = min_val
        self.__elapsed_ticks = 0
        self.__current_bright = 0
        self.__current_dim = 0

    def _update_state(self):
        self.__elapsed_ticks += adafruit_ticks.ticks_ms()


