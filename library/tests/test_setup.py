import mock
import sys


def test_setup(gpio, smbus_notimeout):
    import automationhat
    automationhat.setup()


def test_analog(smbus_notimeout):
    import automationhat
    # VCC = 3.3, GAIN = 4.096, FS = 2.027, Max Voltage = 25.85
    # output ~= ((1 << 11) - 1) / 2047.0 * 2096.0 / 3300.0 * 25.85
    assert round(automationhat.analog.one.read(), 1) == 32.1
    assert round(automationhat.analog.two.read(), 1) == 32.1
    assert round(automationhat.analog.three.read(), 1) == 32.1

    values = automationhat.analog.read()
    for k, v in values.items():
        values[k] = round(v, 1)
    assert values == {'one': 32.1, 'two': 32.1, 'three': 32.1, 'four': 4.1}
