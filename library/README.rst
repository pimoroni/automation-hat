Automation HAT
--------------

|Build Status| |Coverage Status| |PyPi Package| |Python Versions|

https://shop.pimoroni.com/products/automation-hat
https://shop.pimoroni.com/products/automation-phat

Automation HAT/pHAT is a home monitoring and automation controller
featuring relays, analog channels, powered outputs, and buffered inputs
(all 24V tolerant).

Installing
----------

Full install (recommended):
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We've created an easy installation script that will install all
pre-requisites and get your Automation HAT/pHAT up and running with
minimal efforts. To run it, fire up Terminal which you'll find in Menu
-> Accessories -> Terminal on your Raspberry Pi desktop, as illustrated
below:

.. figure:: http://get.pimoroni.com/resources/github-repo-terminal.png
   :alt: Finding the terminal

In the new terminal window type the command exactly as it appears below
(check for typos) and follow the on-screen instructions:

.. code:: bash

    curl https://get.pimoroni.com/automationhat | bash

Alternatively, on Raspbian, you can download the ``pimoroni-dashboard``
and install your product by browsing to the relevant entry:

.. code:: bash

    sudo apt-get install pimoroni

(you will find the Dashboard under 'Accessories' too, in the Pi menu -
or just run ``pimoroni-dashboard`` at the command line)

If you choose to download examples you'll find them in
``/home/pi/Pimoroni/automationhat/``.

Manual install:
~~~~~~~~~~~~~~~

Library install for Python 3:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

on Raspbian:

.. code:: bash

    sudo apt-get install python3-automationhat

other environments:

.. code:: bash

    sudo pip3 install automationhat

Library install for Python 2:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

on Raspbian:

.. code:: bash

    sudo apt-get install python-automationhat

other environments:

.. code:: bash

    sudo pip2 install automationhat

Development:
~~~~~~~~~~~~

If you want to contribute, or like living on the edge of your seat by
having the latest code, you should clone this repository, ``cd`` to the
library directory, and run:

.. code:: bash

    sudo python3 setup.py install

(or ``sudo python setup.py install`` whichever your primary Python
environment may be)

In all cases you will have to enable the i2c bus.

Documentation & Support
-----------------------

-  Guides and tutorials https://learn.pimoroni.com/automation-hat
   https://learn.pimoroni.com/automation-phat
-  Function reference
   https://github.com/pimoroni/automation-hat/tree/master/documentation
-  GPIO Pinout https://pinout.xyz/pinout/automation\_hat
   https://pinout.xyz/pinout/automation\_phat
-  Get help http://forums.pimoroni.com/c/support

.. |Build Status| image:: https://travis-ci.com/pimoroni/automation-hat.svg?branch=master
   :target: https://travis-ci.com/pimoroni/automation-hat
.. |Coverage Status| image:: https://coveralls.io/repos/github/pimoroni/automation-hat/badge.svg?branch=master
   :target: https://coveralls.io/github/pimoroni/automation-hat?branch=master
.. |PyPi Package| image:: https://img.shields.io/pypi/v/automationhat.svg
   :target: https://pypi.python.org/pypi/automationhat
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/automationhat.svg
   :target: https://pypi.python.org/pypi/automationhat
