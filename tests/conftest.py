import sys
import mock
import pytest


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
    sys.modules['smbus'] = mock.MagicMock()
    yield sys.modules['smbus']
    del sys.modules['smbus']


@pytest.fixture(scope='function')
def gpio():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.MagicMock()
    yield
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']