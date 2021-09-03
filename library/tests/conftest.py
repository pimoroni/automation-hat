import sys
import mock
import pytest


class MockSMBus():
    def __init__(self, bus):
        self.regs = {
            0x48: [0 for _ in range(255)],  # ads1015,
            0x54: [0 for _ in range(255)]   # sn3218
        }
        self.regs[0x48][0] = (1 << 11) - 1  # 12-bit ADC, 12th bit is sign

        # Set the uppermost bit of the ADS1015 CONFIG register
        # to indicate an "inactive/start" status
        self.regs[0x48][1] = 0b10000000

    def read_i2c_block_data(self, address, register, length=2):
        if (address, register) == (0x48, 0):
            value = self.regs[address][register:register+(length // 2)]
            return [(value[0] >> 4) & 0xff, (value[0] & 0x0f) << 4]
        return self.regs[address][register:register+length]

    def write_i2c_block_data(self, address, register, data):
        if (address, register) == (0x48, 1):
            return 0
        self.regs[address][register:register+len(data)] = data


@pytest.fixture(scope='function')
def smbus_notimeout():
    sys.modules['smbus'] = mock.Mock()
    sys.modules['smbus'].SMBus = MockSMBus
    yield
    del sys.modules['smbus']


@pytest.fixture(scope='function')
def smbus_timeout():
    sys.modules['smbus'] = mock.Mock()
    sys.modules['smbus'].SMBus = MockSMBus
    yield
    del sys.modules['smbus']


@pytest.fixture(scope='function')
def mocksmbus():
    sys.modules['smbus'] = mock.Mock()
    yield sys.modules['smbus']
    del sys.modules['smbus']


@pytest.fixture(scope='function')
def gpio():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.MagicMock()
    yield
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']