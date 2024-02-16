def test_setup(gpio, smbus, sn3218, automationhat):
    automationhat.setup()


def test_analog(gpio, smbus, sn3218, automationhat):
    automationhat.setup()

    # ads1015.ADS1015().get_voltage.return_value = 3.3

    # VCC = 3.3, GAIN = 4.096, FS = 2.027, Max Voltage = 25.85
    # output ~= ((1 << 11) - 1) / 2047.0 * 2096.0 / 3300.0 * 25.85
    assert round(automationhat.analog.one.read(), 2) == 25.85
    assert round(automationhat.analog.two.read(), 2) == 25.85
    assert round(automationhat.analog.three.read(), 2) == 25.85

    values = automationhat.analog.read()
    for k, v in values.items():
        values[k] = round(v, 2)
    assert values == {'one': 25.85, 'two': 25.85, 'three': 25.85, 'four': 3.3}
