![Automation HAT](https://github.com/pimoroni/automation-hat/blob/main/autohat_360.png)

[![Build Status](https://img.shields.io/github/actions/workflow/status/pimoroni/automation-hat/test.yml?branch=main)](https://github.com/pimoroni/automation-hat/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/automation-hat/badge.svg?branch=main)](https://coveralls.io/github/pimoroni/automation-hat?branch=main)
[![PyPi Package](https://img.shields.io/pypi/v/automationhat.svg)](https://pypi.python.org/pypi/automationhat)
[![Python Versions](https://img.shields.io/pypi/pyversions/automationhat.svg)](https://pypi.python.org/pypi/automationhat)

Automation HAT is a home monitoring and automation controller featuring relays, analog channels, powered outputs, and buffered inputs (all 24V tolerant).  This library will also work with Automation HAT's smaller siblings - Automation pHAT and Automation HAT Mini.

### Where to buy

* Pimoroni Automation HAT: <https://shop.pimoroni.com/products/automation-hat>
* Pimoroni Automation HAT Mini: <https://shop.pimoroni.com/products/automation-hat-mini>
* [DISCONTINUED] Pimoroni Automation pHAT: <https://shop.pimoroni.com/products/automation-phat>

## Installing

### Full install (recommended):

We've created an easy installation script that will install all pre-requisites and get your Automation HAT
up and running with minimal efforts. To run it, fire up Terminal which you'll find in Menu -> Accessories -> Terminal
on your Raspberry Pi desktop, as illustrated below:

![Finding the terminal](http://get.pimoroni.com/resources/github-repo-terminal.png)

In the new terminal window type the command exactly as it appears below (check for typos) and follow the on-screen instructions:

```bash
git clone https://github.com/pimoroni/automation-hat
cd automation-hat
./install.sh
```

**Note** Libraries will be installed in the "pimoroni" virtual environment, you will need to activate it to run examples:

```
source ~/.virtualenvs/pimoroni/bin/activate
```

### Development:

If you want to contribute, or like living on the edge of your seat by having the latest code, you can install the development version like so:

```bash
git clone https://github.com/pimoroni/automation-hat
cd automation-hat
./install.sh --unstable
```

In all cases you will have to enable the I2C bus (and SPI for Automation HAT Mini):

```
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```

## Documentation & Support

* Guides and tutorials:
  * Automation HAT: <https://learn.pimoroni.com/automation-hat>
  * Automation pHAT: <https://learn.pimoroni.com/automation-phat>
  * Automation HAT Mini: <https://learn.pimoroni.com/automation-hat-mini>
* Function reference
<https://github.com/pimoroni/automation-hat/tree/master/documentation>
* GPIO Pinout:
  * Automation HAT: <https://pinout.xyz/pinout/automation_hat>
  * Automation pHAT: <https://pinout.xyz/pinout/automation_phat>
  * Automation HAT Mini: <https://pinout.xyz/pinout/automation_hat_mini>
* Get help
<http://forums.pimoroni.com/c/support>

### FAQ

#### What is the accuracy and resolution of the Automation HAT

The ADS1015 is a 12-bit ADC, but since the 12th bit is the sign-bit there are only 11-bits of resolution available for positive voltage readings. The input voltage for 24v channels is scaled from 0-25.85v (25.85 rather than 24 due to how the resistor divider is set up) to 0-3.3v.

Since the full-scale range of the ADC is set to 4.096v, this means that 0-3.3v gives only ~1649 possible usable values making the input measurement granularity somewhere around 0.015v (25.85 / 1649) for the 24v inputs and 0.002v for the 3.3v input.

More information on this topic can be found here: <https://forums.pimoroni.com/t/automation-hat-accuracy/7252/3>

