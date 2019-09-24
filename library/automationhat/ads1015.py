from functools import wraps
from threading import Lock
import time


def synchronized(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return func(self, *args, **kwargs)

    return wrapper


ADDR = 0x48

REG_CONV = 0x00
REG_CFG = 0x01

SAMPLES_PER_SECOND_MAP = {128: 0x0000, 250: 0x0020, 490: 0x0040, 920: 0x0060, 1600: 0x0080, 2400: 0x00A0, 3300: 0x00C0}
CHANNEL_MAP = {0: 0x4000, 1: 0x5000, 2: 0x6000, 3: 0x7000}
PROGRAMMABLE_GAIN_MAP = {6144: 0x0000, 4096: 0x0200, 2048: 0x0400, 1024: 0x0600, 512: 0x0800, 256: 0x0A00}

PGA_6_144V = 6144
PGA_4_096V = 4096
PGA_2_048V = 2048
PGA_1_024V = 1024
PGA_0_512V = 512
PGA_0_256V = 256


class ads1015:
    def __init__(self, i2c_bus=None, addr=ADDR):
        self._over_voltage = [False] * 4

        self.i2c_bus = i2c_bus
        if not hasattr(i2c_bus, "write_i2c_block_data") or not hasattr(i2c_bus, "read_i2c_block_data"):
            raise TypeError("Object given for i2c_bus must implement write_i2c_block_data and read_i2c_block_data")

        self.addr = addr
        self._lock = Lock()

    @synchronized
    def read(self, channel=0, programmable_gain=PGA_4_096V, samples_per_second=1600):
        """Read a single ADC channel."""
        # sane defaults
        config = 0x0003 | 0x0100

        config |= SAMPLES_PER_SECOND_MAP[samples_per_second]
        config |= CHANNEL_MAP[channel]
        config |= PROGRAMMABLE_GAIN_MAP[programmable_gain]

        # set "single shot" mode
        config |= 0x8000

        delay = (1.0 / samples_per_second) + 0.0001

        # write single conversion flag

        self.i2c_bus.write_i2c_block_data(self.addr, REG_CFG, [(config >> 8) & 0xFF, config & 0xFF])
        time.sleep(delay)
        data = self.i2c_bus.read_i2c_block_data(self.addr, REG_CONV)

        value = ((data[0] << 4) | (data[1] >> 4))

        if value & 0x800:
            value -= 1 << 12

        value /= 2047.0  # Divide down to percentage of FS
        value *= float(programmable_gain)
        value /= 3300.0  # Divide by VCC

        return value

    def read_all(self):
        """Read all ADC values with default settings."""
        return tuple([self.read(channel=x) for x in range(4)])

    values = read_all

    def available(self):
        try:
            self.read()
            return True
        except IOError:
            return False
