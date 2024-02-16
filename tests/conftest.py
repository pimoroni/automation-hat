import sys

import mock
import pytest
from i2cdevice import MockSMBus


class MySMBus(MockSMBus):
    def __init__(self, bus):
        MockSMBus.__init__(self, bus)
        # Set the uppermost bit of the CONFIG register
        # to indicate an "inactive/start" status
        self.regs[0] = [0x67, 0x20]
        self.regs[1] = 0b10000000 | 0b01010000

    def read_i2c_block_data(self, i2c_address, register, length):
        if register in (0x00,):
            return self.regs[register]
        else:
            return self.regs[register:register + length]

    def write_i2c_block_data(self, i2c_address, register, values):
        if register in (0x00,):
            self.regs[register] = values
        else:
            self.regs[register:register + len(values)] = values


@pytest.fixture(scope='function')
def automationhat():
    import automationhat
    yield automationhat
    del sys.modules['automationhat']


@pytest.fixture(scope='function')
def ads1015():
    sys.modules['ads1015'] = mock.MagicMock()
    yield sys.modules['ads1015']
    del sys.modules['ads1015']


@pytest.fixture(scope='function')
def sn3218():
    sys.modules['sn3218'] = mock.MagicMock()
    yield sys.modules['sn3218']
    del sys.modules['sn3218']


@pytest.fixture(scope='function')
def smbus():
    sys.modules["smbus2"] = mock.Mock()
    sys.modules["smbus2"].SMBus = MySMBus
    yield MySMBus
    del sys.modules["smbus2"]


@pytest.fixture(scope='function')
def gpio():
    sys.modules['gpiod'] = mock.Mock()
    sys.modules['gpiod.line'] = mock.Mock()
    sys.modules['gpiodevice'] = mock.MagicMock()
    yield
    del sys.modules['gpiodevice']
    del sys.modules['gpiod.line']
    del sys.modules['gpiod']