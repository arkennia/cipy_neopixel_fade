# (c) Jonathan Manly 2022-
# This source code is licensed under the MIT license.
# See LICENSE for details.

"""
A library for CircuitPython that creates a fade animation using Neopixels.

Reqires:
`adafruit_ticks`
"""
import adafruit_ticks

INCREASING = 0
BRIGHTHOLD = 1
DECREASING = 2
DIMHOLD = 3


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
        self.__create_states()
        self._bright_hold_t = bright_hold_t
        self._bright_t = bright_t
        self._dim_t = dim_t
        self._dim_hold_t = dim_hold_t
        self._max_val = max_val
        self._min_val = min_val
        # The number of ticks it takes before updating the current_bright value.
        self.__bright_step_ticks = bright_t // (max_val - min_val)
        # The number of ticks it takes before updating the current_dim value.
        self.__dim_step_ticks = dim_t // (max_val - min_val)
        # Elapsed number of ticks for the current state.
        self.__elapsed_ticks = 0
        # The current value of the brightness. Im not sure if I need
        # current bright and dim.
        self.__current_bright = 0
        # Records the current state.
        self.__current_state = INCREASING
        # The number of ticks to stay in the current state.
        self.__current_state_ticks = 0

    def update(self):
        """
        Update the class, checking if enough time has passed to update any states.

        Returns:
            The current brightness value.
        """
        self.__elapsed_ticks += adafruit_ticks.ticks_ms()

        # Return true iff current state ticks is less than elapsed ticks,
        # assuming that they are within 2**28 ticks.
        if adafruit_ticks.ticks_less(self.__current_state_ticks, self.__elapsed_ticks):
            self.__elapsed_ticks = 0
            self._update_state()
        return self.__current_bright

    def _update_state(self):
        self.STATES[self.__current_state]()

    def __create_states(self):
        """Create the self.STATES dict."""
        self.STATES = {
            INCREASING: self.__increasing_state,
            BRIGHTHOLD: self.__brighthold_state,
            DECREASING: self.__decreasing_state,
            DIMHOLD: self.__dimhold_state
        }

    def __increasing_state(self):
        if self.__current_bright >= self._max_val:
            self.__current_state = BRIGHTHOLD
            self.__current_state_ticks = self._bright_hold_t
        else:
            self.__current_bright += 1

    def __brighthold_state(self):
        self.__current_state = DECREASING
        self.__current_state_ticks = self.__dim_step_ticks

    def __dimhold_state(self):
        self.__current_state = INCREASING
        self.__current_state_ticks = self.__bright_step_ticks

    def __decreasing_state(self):
        if self.__current_bright <= self._min_val:
            self.__current_state = DIMHOLD
            self.__current_state_ticks = self._dim_hold_t
        else:
            self.__current_bright -= 1
