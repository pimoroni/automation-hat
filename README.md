![Automation HAT](autohat_360.png)

[![Build Status](https://travis-ci.com/pimoroni/automation-hat.svg?branch=master)](https://travis-ci.com/pimoroni/automation-hat)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/automation-hat/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/automation-hat?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/automationhat.svg)](https://pypi.python.org/pypi/automationhat)
[![Python Versions](https://img.shields.io/pypi/pyversions/automationhat.svg)](https://pypi.python.org/pypi/automationhat)


https://shop.pimoroni.com/products/automation-hat
https://shop.pimoroni.com/products/automation-phat

Automation HAT/pHAT is a home monitoring and automation controller featuring relays, analog channels, powered outputs, and buffered inputs (all 24V tolerant).

## Installing

### Full install (recommended):

We've created an easy installation script that will install all pre-requisites and get your Automation HAT/pHAT
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

### Manual install:

#### Library install for Python 3:

on Raspbian:

```bash
sudo apt-get install python3-automationhat
```

other environments:

```bash
sudo pip3 install automationhat
```

#### Library install for Python 2:

on Raspbian:

```bash
sudo apt-get install python-automationhat
```

other environments:

```bash
sudo pip2 install automationhat
```

### Development:

If you want to contribute, or like living on the edge of your seat by having the latest code, you should clone this repository, `cd` to the library directory, and run:

```bash
sudo python3 setup.py install
```
(or `sudo python setup.py install` whichever your primary Python environment may be)

In all cases you will have to enable the i2c bus.

## Documentation & Support

* Guides and tutorials
https://learn.pimoroni.com/automation-hat
https://learn.pimoroni.com/automation-phat
* Function reference
https://github.com/pimoroni/automation-hat/tree/master/documentation
* GPIO Pinout
https://pinout.xyz/pinout/automation_hat
https://pinout.xyz/pinout/automation_phat
* Get help
http://forums.pimoroni.com/c/support
