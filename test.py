#!/usr/bin/env python

import sys
import time

import mock

pinstates = [0 for x in range(40)]

def rpi_gpio_output(pin, value):
    global pinstates
    pinstates[pin] = value


def rpi_gpio_input(pin):
    return pinstates[pin]


rpi = mock.Mock()
rpi.GPIO = mock.Mock()
rpi.GPIO.input = rpi_gpio_input
rpi.GPIO.output = rpi_gpio_output

sys.modules['RPi'] = rpi
sys.modules['RPi.GPIO'] = 0 # Fix RPi.GPIO import error insanity

sn3218 = mock.Mock()
sn3218.i2c = mock.Mock()
sn3218.i2c.read_i2c_block_data = mock.Mock(return_value=[0,0,0])

sys.modules['sn3218'] = sn3218

import automationhat  # noqa: E402


def test(verbose=False):

    def gpio_set(pin, value):
        global pinstates
        pinstates[pin] = value

    def debug(msg):
        if verbose:
            print(msg)

    debug("testing: Lights")

    assert sorted(str(automationhat.light).split(", ")) == ["comms", "power", "warn"], "Lights missing one of [warn, comms, power]: {}".format(str(automationhat.light))

    for light in automationhat.light:
        debug("         light {}".format(light.name))

        assert callable(light.write), "light.write() not callable"
        assert callable(light.toggle), "light.toggle() not callable"
        assert callable(light.on), "light.on() not callable"
        assert callable(light.off), "light.off() not callable"


    debug("testing: Relays")

    assert str(automationhat.relay).split(", ") == ["one","two","three"], "Relay missing one of [one, two, three]: {}".format(str(automationhat.relay))

    # Test all relays have associated lights
    for relay in automationhat.relay:
        debug("         relay {}".format(relay.name))

        assert isinstance(relay.light_no, automationhat.SNLight), "Relay missing NO light"
        assert isinstance(relay.light_nc, automationhat.SNLight), "Relay missing NC light"

        assert callable(relay.on), "relay.on() not callable"
        relay.on() # Should transition from LOW to HIGH
        assert pinstates[relay.pin] == 1, "pin {} not set HIGH for Relay {}".format(relay.pin, relay.name)

        assert callable(relay.off), "relay.off() not callable"
        relay.off() # Should transition from HIGH to LOW
        assert pinstates[relay.pin] == 0, "pin {} not set LOW for Relay {}".format(relay.pin, relay.name)

        assert callable(relay.toggle), "relay.toggle() not callable"
        relay.toggle() # Should transition from LOW to HIGH
        assert pinstates[relay.pin] == 1, "pin {} not set HIGH for Relay {}".format(relay.pin, relay.name)
        relay.toggle() # Should transition from HIGH to LOW
        assert pinstates[relay.pin] == 0, "pin {} not set LOW for Relay {}".format(relay.pin, relay.name)


    debug("testing: Digital Outputs")

    assert str(automationhat.output).split(", ") == ["one","two","three"], "Output missing one of [one, two, three]: {}".format(str(automationhat.output))

    # Test all outputs have associated lights
    for output in automationhat.output:
        debug("         output {}".format(output.name))

        assert isinstance(output.light, automationhat.SNLight), "Missing SNLight from output"
        output.on()
        assert pinstates[output.pin] == 1, "pin {} not set HIGH for Output {}".format(output.pin, output.name)
        output.off()
        assert pinstates[output.pin] == 0, "pin {} not set LOW for Output {}".format(output.pin, output.name)

    debug("testing: Digital Inputs")

    # Test all inputs have associated lights
    for input in automationhat.input:
        debug("         input {}".format(input.name))

        assert callable(input.read), "input.read() not callable!"
        assert input.read() == 0, "Input reading HIGH, should be LOW"
        gpio_set(input.pin, 1)
        assert input.read() == 1, "Input reading LOW, should be HIGH"
        assert isinstance(input.light, automationhat.SNLight), "Missing SNLight from input"


    debug("testing: Analog Inputs")

    automationhat._ads1015.get_voltage = mock.MagicMock()

    for analog in automationhat.analog:
        debug("         analog {}".format(analog.name))

        analog.auto_light(False)
        assert analog._en_auto_lights is False, "Auto lights should be False/Disabled"

        analog.auto_light(True)
        assert analog._en_auto_lights is True, "Auto lights should be True/Enabled"


        assert callable(analog.read), "analog.read() not callable!"

        # The full scale range of the ADC at 1:1 is +- 4.096v
        # so we adjust our mock value to obtain the max value at 3.3v
        # analog_raw = int(3300.0 * (2047.0 / 4096.0))

        debug("         - max value")

        automationhat._ads1015.get_voltage.return_value = 3.3

        time.sleep(0.01)

        assert analog.read() == analog.max_voltage, "analog.read() returning {}, should be {}!".format(analog.read(), analog.max_voltage)

        # analog_raw = int(1650.0 * (2047.0 / 4096.0))

        debug("         - half value")

        automationhat._ads1015.get_voltage.return_value = 3.3 / 2.0001  # TODO: Fudge!

        time.sleep(0.01)

        voltage = round((analog.max_voltage / 2.0) - 0.005, 2)
        assert round(analog.read(), 2) == voltage, "analog.read() returning {}, should be {}!".format(round(analog.read(), 2), voltage)


    debug("status:  Ok!")

    return True

if __name__ == "__main__":
    test(verbose=True)
