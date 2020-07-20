import mock
import sys


class MockSMBus():
    def __init__(self, bus):
        self.regs = {
            0x48: [0 for _ in range(255)],  # ads1015,
            0x54: [0 for _ in range(255)]   # sn3218
        }
        self.regs[0x48][0] = (1 << 11) - 1  # 12-bit ADC, 12th bit is sign

    def read_i2c_block_data(self, address, register, length=2):
        if address == 0x48:
            value = self.regs[address][register:register+(length // 2)]
            return [(value[0] >> 4) & 0xff, (value[0] & 0x0f) << 4]
        return self.regs[address][register:register+length]

    def write_i2c_block_data(self, address, register, data):
        self.regs[address][register:register+len(data)] = data


def test_setup():
    sys.modules['smbus'] = mock.Mock()
    sys.modules['smbus'].SMBus = MockSMBus
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.MagicMock()
    import automationhat
    automationhat.setup()


def test_analog():
    sys.modules['smbus'] = mock.Mock()
    sys.modules['smbus'].SMBus = MockSMBus
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.MagicMock()
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
