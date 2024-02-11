# SPDX-FileCopyrightText: 2019 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython PCF8574 Interrupts example

Any pin that is set HIGH is in input mode and will fire an interrupt on the INT pin
on any rising or falling edge.

Interrupt is cleared when the pins are changed or the port is read.

Add a push button between pin P07 and GND. Works on any pin. P07 picked at random.

When pressed P07 will be driven LOW and the interrupt will fire.

When released another interrupt will fire, if the previous interrupt has been cleared.

Debouncing
----------

In some cases, debouncing isn't required. Depends on the hardware.

If you add a 100nF capacitor across the push button, it will add a
bit of a buffer and block rapid fires. 100nF blocks for around a second.
A 10nF capacitor blocks for roughly 1/10th of a second.
"""

import pcf8574
from machine import I2C, Pin

# TinyPICO (ESP32)
i2c = I2C(0)

pcf = pcf8574.PCF8574(i2c, 0x20)

# set all pins as inputs (HIGH)
pcf.port = 0xFF

# attach an IRQ to any mcu pin that can be pulled high.
# INT is open drain, so the mcu pin needs a pull-up
# when the INT pin activates, it will go LOW
p4 = Pin(4, Pin.IN, Pin.PULL_UP)


# a simple interrupt handler
def _handler(p):
    print(f"INT: {p.value()}, PORT: {pcf.port}")


# turn on interrupt handler
p4.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=_handler)

# turn off interrupt handler
p4.irq(None)
