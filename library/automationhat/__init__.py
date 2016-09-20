import time
import atexit
import sn3218

from ads1015 import ads1015
import RPi.GPIO as GPIO
from pins import ObjectCollection, AsyncWorker, StoppableThread


RELAY_1 = 13
RELAY_2 = 19
RELAY_3 = 16

INPUT_1 = 26
INPUT_2 = 20
INPUT_3 = 21

OUTPUT_1 = 5
OUTPUT_2 = 12
OUTPUT_3 = 6

ads1015 = ads1015(sn3218.i2c)

_led_states = [0] * 18
_led_dirty = False

sn3218.enable()
sn3218.enable_leds(0b111111111111111111)

class SNLight(object):
    def __init__(self, index):
        self.index = index
        self._max_brightness = float(128)

    def toggle(self):
        """Toggle the light from on to off or off to on"""
        self.write((self._max_brightness - self.read()) / self._max_brightness)

    def on(self):
        """Turn the light on"""
        self.write(1)

    def off(self):
        """Turn the light off"""
        self.write(0)

    def read(self):
        """Read the current status of the light"""
        if self.index is None:
            return

        return _led_states[self.index]

    def write(self, value):
        """Write a specific value to the light

        :param value: Brightness of the light, from 0.0 to 1.0
        """
        global _led_dirty
        if self.index is None:
            return

        if type(value) is int and value >= 0 and value <= 1.0:
            _led_states[self.index] = int(self._max_brightness * value)
            _led_dirty = True


class AnalogInput(object):
    type = 'Analog Input'

    def __init__(self, channel, max_voltage, led):
        self._en_auto_lights = True
        self.channel = channel
        self.value = 0
        self.max_voltage = float(max_voltage)
        self.light = SNLight(led)

    def auto_light(self, value):
        self._en_auto_lights = value
        return True

    def read(self):
        """Return the read voltage of the analog input"""
        return self.value * self.max_voltage

    def _update(self):
        self.value = ads1015.read(self.channel)

    def _auto_lights(self):
        if self._en_auto_lights:
            adc = self.value
            self.light.write(max(0.0,min(1.0,adc)))


class Pin(object):
    type = 'Pin'

    def __init__(self, pin):
        self.pin = pin
        self._last_value = None

    def __call__(self):
        return filter(lambda x: x[0] != '_', dir(self))

    def read(self):
        return GPIO.input(self.pin)

    def has_changed(self):
        value = self.read()

        if self._last_value is None:
            self._last_value = value

        if value is not self._last_value:
            self._last_value = value
            return True

        return False

    def is_on(self):
        return self.read() == 1

    def is_off(self):
        return self.read() == 0


class Input(Pin):
    type = 'Digital Input'

    def __init__(self, pin, led):
        self._en_auto_lights = True
        Pin.__init__(self, pin)
        GPIO.setup(self.pin, GPIO.IN)
        self.light = SNLight(led)

    def auto_light(self, value):
        self._en_auto_lights = value
        return True

    def _auto_lights(self):
        if self._en_auto_lights:
            self.light.write(self.read()) 


class Output(Pin):
    type = 'Digital Output'

    def __init__(self, pin, led):
        self._en_auto_lights = True
        Pin.__init__(self, pin)
        GPIO.setup(self.pin, GPIO.OUT)
        self.light = SNLight(led)

    def auto_light(self, value):
        self._en_auto_lights = value
        return True

    def write(self, value):
        """Write a value to the output.

        :param value: Value to write, either 1 for HIGH or 0 for LOW
        """
        GPIO.output(self.pin, value)
        if self._en_auto_lights:
            self.light.write(value)

    def on(self):
        """Turn the output on/HIGH"""
        self.write(1)

    def off(self):
        """Turn the output off/LOW"""
        self.write(0)

    def toggle(self):
        """Toggle the output."""
        self.write(not self.read())


class Relay(Output):
    type = 'Relay'

    def __init__(self, pin, led_no, led_nc):
        Pin.__init__(self, pin)
        GPIO.setup(self.pin, GPIO.OUT)
        self.light_no = SNLight(led_no)
        self.light_nc = SNLight(led_nc)

    def write(self, value):
        """Write a value to the relay.

        :param value: Value to write, either 0 for LOW or 1 for HIGH
        """
        GPIO.output(self.pin, value)

        if value:
            self.light_no.write(1)
            self.light_nc.write(0)
        else:
            self.light_no.write(0)
            self.light_nc.write(1)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

analog = ObjectCollection()
analog._add(one=AnalogInput(0, 25.85, 0))
analog._add(two=AnalogInput(1, 25.85, 1))
analog._add(three=AnalogInput(2, 25.85, 2))
analog._add(four=AnalogInput(3, 3.3, None))

input = ObjectCollection()
input._add(one=Input(INPUT_1, 14))
input._add(two=Input(INPUT_2, 13))
input._add(three=Input(INPUT_3, 12))

output = ObjectCollection()
output._add(one=Output(OUTPUT_1, 3))
output._add(two=Output(OUTPUT_2, 4))
output._add(three=Output(OUTPUT_3, 5))

relay = ObjectCollection()
relay._add(one=Relay(RELAY_1, 6, 7))
relay._add(two=Relay(RELAY_2, 8, 9))
relay._add(three=Relay(RELAY_3, 10, 11))

light = ObjectCollection()
light._add(power=SNLight(17))
light._add(comms=SNLight(16))
light._add(warn=SNLight(15))

def _update_adc():
    analog._update()
    time.sleep(0.001)

def _auto_lights():
    global _led_dirty

    input._auto_lights()
    analog._auto_lights()

    if _led_dirty:
        sn3218.output(_led_states)
        _led_dirty = False

    time.sleep(0.01)

_t_auto_lights = AsyncWorker(_auto_lights)
_t_auto_lights.start()

_t_update_adc = AsyncWorker(_update_adc)
_t_update_adc.start()

def _cleanup():
    _t_auto_lights.stop()
    _t_update_adc.stop()
    GPIO.cleanup()
    sn3218.output([0] * 18)

atexit.register(_cleanup)
