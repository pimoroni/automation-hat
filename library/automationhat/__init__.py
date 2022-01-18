import atexit
import time
import warnings

try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError("This library requires the RPi.GPIO module\nInstall with: sudo python3 -m pip install RPi.GPIO")

try:
    import smbus
except ImportError:
    raise ImportError("This library requires python3-smbus\nInstall with: sudo apt install python3-smbus")

try:
    import ads1015
except ImportError:
    raise ImportError("This library requires ads1015\nInstall with: sudo python3 -m pip install ads1015")

from .pins import ObjectCollection, AsyncWorker, StoppableThread

__version__ = '0.4.0'


RELAY_1 = 13
RELAY_2 = 19
RELAY_3 = 16

INPUT_1 = 26
INPUT_2 = 20
INPUT_3 = 21

OUTPUT_1 = 5
OUTPUT_2 = 12
OUTPUT_3 = 6

UPDATES_PER_SECOND = 30

i2c = None
sn3218 = None

automation_hat = False
automation_phat = True

_led_states = [0] * 18
_lights_need_updating = False
_is_setup = False
_t_update_lights = None
_ads1015 = None


class SNLight(object):
    def __init__(self, index):
        self.index = index
        self._max_brightness = float(128)

    def toggle(self):
        """Toggle the light from on to off or off to on"""
        self.write(1 - self.read())

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

        return _led_states[self.index] / self._max_brightness

    def write(self, value):
        """Write a specific value to the light

        :param value: Brightness of the light, from 0.0 to 1.0
        """
        global _lights_need_updating

        if self.index is None:
            return

        if type(value) is not int and type(value) is not float:
            raise TypeError("Value must be int or float")

        if value >= 0 and value <= 1.0:
            _led_states[self.index] = int(self._max_brightness * value)
            if _t_update_lights is None and sn3218 is not None:
                sn3218.output(_led_states)
            else:
                _lights_need_updating = True

        else:
            raise ValueError("Value must be between 0.0 and 1.0")


class AnalogInput(object):
    type = 'Analog Input'

    def __init__(self, channel, max_voltage, led):
        self._en_auto_lights = True
        self.channel = channel
        self.value = 0
        self.max_voltage = float(max_voltage)
        self.light = SNLight(led)
        self._is_setup = False

    def setup(self):
        if self._is_setup:
            return

        setup()
        self._is_setup = True

    def auto_light(self, value=None):
        if value is not None:
            self._en_auto_lights = value
        return self._en_auto_lights

    def read(self):
        """Return the read voltage of the analog input"""
        if self.name == "four" and is_automation_phat():
            warnings.warn("Analog Four is not supported on Automation pHAT")

        self._update()
        return round(self.value * self.max_voltage, 3)

    def _update(self):
        self.setup()
        self.value = _ads1015.get_voltage("in{}/gnd".format(self.channel)) / 3.3

        if self._en_auto_lights:
            adc = self.value
            self.light.write(max(0.0, min(1.0, adc)))


class Pin(object):
    type = 'Pin'

    def __init__(self, pin):
        self.pin = pin
        self._last_value = None
        self._is_setup = False

    def __call__(self):
        return filter(lambda x: x[0] != '_', dir(self))

    def read(self):
        self.setup()
        return GPIO.input(self.pin)

    def setup(self):
        pass

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
        self.light = SNLight(led)

    def setup(self):
        if self._is_setup:
            return False

        setup()
        GPIO.setup(self.pin, GPIO.IN)
        self._is_setup = True

    def auto_light(self, value=None):
        if value is not None:
            self._en_auto_lights = value
        return self._en_auto_lights

    def read(self):
        value = Pin.read(self)
        if self._en_auto_lights:
            self.light.write(value)
        return value


class Output(Pin):
    type = 'Digital Output'

    def __init__(self, pin, led):
        self._en_auto_lights = True
        Pin.__init__(self, pin)
        self.light = SNLight(led)

    def setup(self):
        if self._is_setup:
            return False

        setup()
        GPIO.setup(self.pin, GPIO.OUT, initial=0)
        self._is_setup = True
        return True

    def auto_light(self, value=None):
        if value is not None:
            self._en_auto_lights = value
        return self._en_auto_lights

    def write(self, value):
        """Write a value to the output.

        :param value: Value to write, either 1 for HIGH or 0 for LOW
        """
        self.setup()
        GPIO.output(self.pin, value)
        if self._en_auto_lights:
            self.light.write(1 if value else 0)

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
        self.light_no = SNLight(led_no)
        self.light_nc = SNLight(led_nc)
        self._en_auto_lights = True

    def auto_light(self, value=None):
        if value is not None:
            self._en_auto_lights = value
        return self._en_auto_lights

    def setup(self):
        if self._is_setup:
            return False

        setup()

        if is_automation_phat() and self.name == "one":
            self.pin = RELAY_3

        GPIO.setup(self.pin, GPIO.OUT, initial=0)
        self._is_setup = True
        return True

    def write(self, value):
        """Write a value to the relay.

        :param value: Value to write, either 0 for LOW or 1 for HIGH
        """
        self.setup()

        if is_automation_phat() and self.name in ["two", "three"]:
            warnings.warn("Relay '{}' is not supported on Automation pHAT".format(self.name))

        GPIO.output(self.pin, value)

        if self._en_auto_lights:
            if value:
                self.light_no.write(1)
                self.light_nc.write(0)
            else:
                self.light_no.write(0)
                self.light_nc.write(1)


def _update_lights():
    global _lights_need_updating

    analog.read()
    input.read()

    if _lights_need_updating:
        sn3218.output(_led_states)
        _lights_need_updating = False

    time.sleep(1.0 / UPDATES_PER_SECOND)


def is_automation_hat():
    setup()
    return sn3218 is not None


def is_automation_phat():
    setup()
    return sn3218 is None


def enable_auto_lights(state):
    global _t_update_lights

    setup()

    if sn3218 is None:
        return

    input.auto_light(state)
    output.auto_light(state)
    relay.auto_light(state)
    analog.auto_light(state)

    if state and _t_update_lights is None:
        _t_update_lights = AsyncWorker(_update_lights)
        _t_update_lights.start()

    if not state and _t_update_lights is not None:
        _t_update_lights.stop()
        _t_update_lights.join()
        _t_update_lights = None


def setup():
    global automation_hat, automation_phat, sn3218, _ads1015, _is_setup, _t_update_lights

    if _is_setup:
        return True

    _is_setup = True

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    _ads1015 = ads1015.ADS1015()
    try:
        chip_type = _ads1015.detect_chip_type()
    except IOError:
        raise RuntimeError("No ADC detected, check your connections")

    if chip_type == 'ADS1015':
        _ads1015.set_sample_rate(1600)
    else:
        _ads1015.set_sample_rate(860)

    _ads1015.set_programmable_gain(4.096)

    try:
        import sn3218
    except ImportError:
        raise ImportError("This library requires sn3218\nInstall with: sudo python3 -m pip install sn3218")
    except IOError:
        pass

    if sn3218 is not None:
        sn3218.enable()
        sn3218.enable_leds(0b111111111111111111)
        automation_hat = True
        automation_phat = False
        _t_update_lights = AsyncWorker(_update_lights)
        _t_update_lights.start()

    atexit.register(_exit)


def _exit():
    if _t_update_lights:
        _t_update_lights.stop()
        _t_update_lights.join()

    if sn3218 is not None:
        sn3218.output([0] * 18)

    GPIO.cleanup()


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

