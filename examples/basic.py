# SPDX-FileCopyrightText: 2019 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython PCF8574 Basic example

Toggles pins individually, then all in a single call
"""

import pcf8574
from machine import I2C

# TinyPICO (ESP32)
i2c = I2C(0)

pcf = pcf8574.PCF8574(i2c, 0x20)

# read pin 2
pcf.pin(2)

# set pin 3 HIGH
pcf.pin(3, 1)

# set pin 4 LOW
pcf.pin(4, 0)

# toggle pin 5
pcf.toggle(5)

# set all pins at once with 8-bit int
pcf.port = 0xFF

# read all pins at once as 8-bit int
print(pcf.port)
# returns 255 (0xFF)
