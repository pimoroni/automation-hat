![Automation HAT](autohat_360.png)

[![Build Status](https://travis-ci.com/pimoroni/automation-hat.svg?branch=master)](https://travis-ci.com/pimoroni/automation-hat)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/automation-hat/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/automation-hat?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/automationhat.svg)](https://pypi.python.org/pypi/automationhat)
[![Python Versions](https://img.shields.io/pypi/pyversions/automationhat.svg)](https://pypi.python.org/pypi/automationhat)

Automation HAT is a home monitoring and automation controller featuring relays, analog channels, powered outputs, and buffered inputs (all 24V tolerant).  This library will also work with Automation HAT's smaller siblings - Automation pHAT and Automation HAT Mini.

### Where to buy

* Pimoroni Automation HAT: <https://shop.pimoroni.com/products/automation-hat>
* Pimoroni Automation HAT Mini: <https://shop.pimoroni.com/products/automation-hat-mini>
* [DISCONTINUED] Pimoroni Automation pHAT: <https://shop.pimoroni.com/products/automation-phat>

## Installing

### Full install (recommended)

We've created an easy installation script that will install all pre-requisites and get your Automation HAT, pHAT or HAT Mini
up and running with minimal efforts. To run it, fire up Terminal which you'll find in Menu -> Accessories -> Terminal
on your Raspberry Pi desktop, as illustrated below:

![Finding the terminal](http://get.pimoroni.com/resources/github-repo-terminal.png)

In the new terminal window type the command exactly as it appears below (check for typos) and follow the on-screen instructions:

```bash
curl https://get.pimoroni.com/automationhat | bash
```

Alternatively, on Raspbian, you can download the `pimoroni-dashboard` and install your product by browsing to the relevant entry:

```bash
sudo apt-get install pimoroni
```

(you will find the Dashboard under 'Accessories' too, in the Pi menu - or just run `pimoroni-dashboard` at the command line)

If you choose to download examples you'll find them in `/home/pi/Pimoroni/automationhat/`.

### Manual install

#### Library install for Python 3

on Raspbian:

```bash
sudo apt-get install python3-automationhat
```

other environments:

```bash
sudo pip3 install automationhat
```

#### Library install for Python 2

on Raspbian:

```bash
sudo apt-get install python-automationhat
```

other environments:

```bash
sudo pip2 install automationhat
```

### Development

If you want to contribute, or like living on the edge of your seat by having the latest code, you should clone this repository, `cd` to the library directory, and run:

```bash
sudo python3 setup.py install
```

(or `sudo python setup.py install` whichever your primary Python environment may be)

In all cases you will have to enable the i2c bus.

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

# Changelog
0.4.0
-----

* Switch to ADS1X15 library

0.3.0
-----

* Switch to setup.cfg
* Switch to markdown based README
* Support for ADS1115 board variant

0.2.3
-----

* 0.2.2 + bump for newer examples

0.2.2
-----

* Had ST7789 on the brain, swapped for ST7735

0.2.1
-----

* Add dependency on ST7789 for AMH

0.2.0
-----

* Fix: Fix thread interleaving and race conditions leading to spurious ADC readings
* Fix: Switch to non-deprecated alias of thread.isAlive

0.1.0
-----

* Fix: Defer setup to avoid import side effects
* Fix: Slowed LED update rate
* Improvement: Switched to warnings to notify about unsupported features on pHAT

0.0.4
-----

* Fix for HAT/pHAT detection

0.0.3
-----

* Fix for Python 3 support

0.0.2
-----

* Added pHAT support
* Rounded ADC output to 2 decimal places
* Set initial state for outputs and fixed toggling
* Fixed light toggling

0.0.1
-----

* Initial Release

