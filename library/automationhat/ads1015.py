from functools import wraps
from threading import Lock
import time


try:
    ADS1015TimeoutError = TimeoutError
except NameError:
    from socket import timeout as ADS1015TimeoutError


def synchronized(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return func(self, *args, **kwargs)

    return wrapper


ADDR = 0x48

REG_CONV = 0x00
REG_CFG = 0x01

# Only accurate for ADS1015
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

    def busy(self):
        data = self.i2c_bus.read_i2c_block_data(self.addr, REG_CFG)
        status = (data[0] << 8) | data[1]
        return (status & (1 << 15)) == 0

    @synchronized
    def read(self, channel=0, timeout=5.0):
        """Read a single ADC channel."""
        programmable_gain = PGA_4_096V
        samples_per_second = 250

        # sane defaults
        config = 0x0003 | 0x0100

        config |= SAMPLES_PER_SECOND_MAP[samples_per_second]
        config |= CHANNEL_MAP[channel]
        config |= PROGRAMMABLE_GAIN_MAP[programmable_gain]

        # set "single shot" mode
        config |= 0x8000

        # write single conversion flag
        self.i2c_bus.write_i2c_block_data(self.addr, REG_CFG, [(config >> 8) & 0xFF, config & 0xFF])

        # Time the ADC conversion to disambiguate ADS1015 from ADS1115
        # Genius out of the box thinking by Niko
        # the ADS1015 will run this at 250SPS
        # the ADS1115 will run this at 16!!! SPS
        # Since the difference is ~an order of magnitude~ they're easy to tell apart.
        t_start = time.time()

        while self.busy():
            # We've got a lock on the I2S bus, but probably don't want to hog it!
            time.sleep(1.0 / 160)
            if time.time() - t_start > timeout:
                raise ADS1015TimeoutError("Timed out waiting for conversion.")

        t_end = time.time()
        t_elapsed = t_end - t_start

        data = self.i2c_bus.read_i2c_block_data(self.addr, REG_CONV)

        if t_elapsed < 1.0 / 16: # 1/16th second is ADS1115 speed, if it's faster it must be an ADS1015
            # 12-bit
            value = (data[0] << 4) | (data[1] >> 4)

            if value & 0x800:  # Check and apply sign bit
                value -= 1 << 12

            value /= 2047.0  # Divide by full scale range

        else: # If it's slower than "ideal" ADS1115 then it's an ADS1115
            # 16-bit
            value = (data[0] << 8) | data[1]

            if value & 0x8000:  # Check and apply sign bit
                value -= 1 << 16

            value /= 32767.0  # Divide by full scale rane

        value *= float(programmable_gain)  # Multiply by gain 
        value /= 3300.0  # Divide by supply voltage

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

