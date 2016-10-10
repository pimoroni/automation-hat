#!/usr/bin/env python
import sys

import mock

pinstates = [0 for x in range(40)]

def rpi_gpio_output(pin, value):
    global pinstates
    pinstates[pin] = value
    #debug("Setting {} to {}".format(pin, value))

def rpi_gpio_input(pin):
    return pinstates[pin]

def sn3218_write_i2c_block_data(addr, reg, data):
    debug("Writing {} to {}:{}".format(data, addr, reg))

rpi = mock.Mock()
rpi.GPIO = mock.Mock()
rpi.GPIO.input = rpi_gpio_input # mock.Mock(return_value=0)
rpi.GPIO.output = rpi_gpio_output

sys.modules['RPi'] = rpi
sys.modules['RPi.GPIO'] = 0 # Fix RPi.GPIO import error insanity

sn3218 = mock.Mock()
sn3218.i2c = mock.Mock()
sn3218.i2c.read_i2c_block_data = mock.Mock(return_value=[0,0,0])
#sn3218.i2c.write_i2c_block_data = sn3218_write_i2c_block_data

sys.modules['sn3218'] = sn3218

import RPi.GPIO

import automationhat

def test(verbose=False):
    def debug(msg):
        if verbose:
            print(msg)

    debug("--Lights--")
    assert str(automationhat.light).split(", ") == ["warn","comms","power"], "Lights missing one of [warn, comms, power]: {}".format(str(automationhat.light))
    debug(automationhat.light)

    # Test write/toggle
    try:
        assert type(automationhat.light.write(1)) == dict, "light.write(1) not returning dict"
        assert type(automationhat.light.write(0)) == dict, "light.write(0) not returning dict"
        assert type(automationhat.light.toggle()) == dict, "light.toggle() not returning dict"
        assert type(automationhat.light.toggle()) == dict, "light.toggle() not returning dict"
        assert type(automationhat.light.on()) == dict, "light.oncd ,8() not returning dict"
        assert type(automationhat.light.off()) == dict, "light.off() not returning dict"
    except Exception as e:
        sys.exit("ERROR: {}".format(e))

    debug("")

    debug("--Relays--")
    debug(automationhat.relay)

    assert str(automationhat.relay).split(", ") == ["three","two","one"], "Relay missing one of [one, two, three]: {}".format(str(automationhat.relay))

    # Test all relays have associated lights
    for relay in automationhat.relay:
        assert isinstance(relay.light_no, automationhat.SNLight), "Relay missing NO light"
        assert isinstance(relay.light_nc, automationhat.SNLight), "Relay missing NC light"

    try:
        debug("Turning relays on...")
        assert type(automationhat.relay.write(1)) == dict, "relay.write(1) not returning dict"
        for relay in automationhat.relay:
            assert pinstates[relay.pin] == 1, "pin {} not set HIGH for Relay {}".format(relay.pin, relay.name)

        debug("Turning relays off...") 
        assert type(automationhat.relay.write(0)) == dict, "relay.write(0) not returning dict"
        for relay in automationhat.relay:
            assert pinstates[relay.pin] == 0, "pin {} not set LOW for Relay {}".format(relay.pin, relay.name)

        debug("Toggling relays...")
        assert type(automationhat.relay.toggle()) == dict, "relay.toggle() not returning dict"
        for relay in automationhat.relay:
            assert pinstates[relay.pin] == 1, "pin {} not set HIGH for Relay {}".format(relay.pin, relay.name)

        debug("Toggling relays again...")
        assert type(automationhat.relay.toggle()) == dict, "relay.toggle() not returning dict"
        for relay in automationhat.relay:
            assert pinstates[relay.pin] == 0, "pin {} not set LOW for Relay {}".format(relay.pin, relay.name)

    except Exception as e:
        sys.exit("ERROR: {}".format(e))

    debug("")

    debug("--Digital Outputs--")
    assert str(automationhat.output).split(", ") == ["three","two","one"], "Output missing one of [one, two, three]: {}".format(str(automationhat.output))
    debug(automationhat.output)

    # Test all outputs have associated lights
    for output in automationhat.output:
        assert isinstance(output.light, automationhat.SNLight), "Missing SNLight from output"

    debug("")

    debug("--Digital Inputs--")
    debug(automationhat.input)
    assert automationhat.input.one.read() == 0, "Input reading HIGH, should be LOW"
    debug(automationhat.input.read())

    # Test all inputs have associated lights
    for input in automationhat.input:
        assert isinstance(input.light, automationhat.SNLight), "Missing SNLight from input"

    debug("")

    debug("--Analog Inputs--")
    debug(automationhat.analog)

    automationhat.analog.auto_light(False)
    assert automationhat.analog.one._en_auto_lights == False, "Auto lights should be False/Disabled"

    automationhat.analog.auto_light(True)
    assert automationhat.analog.one._en_auto_lights == True, "Auto lights should be True/Enabled"

    debug(automationhat.analog.read())
    debug("")
    debug("ALL OKAY!")
    return True

if __name__ == "__main__":
    test(verbose=True)
