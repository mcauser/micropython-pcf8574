# SPDX-FileCopyrightText: 2019 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython PCF8574 8-Bit I2C I/O Expander with Interrupt
https://github.com/mcauser/micropython-pcf8574
"""

__version__ = "1.1.0"


class PCF8574:
    def __init__(self, i2c, address=0x20):
        self._i2c = i2c
        self._address = address
        self._port = bytearray(1)

    def check(self):
        if self._i2c.scan().count(self._address) == 0:
            raise OSError(f"PCF8574 not found at I2C address {self._address:#x}")
        return True

    @property
    def port(self):
        self._read()
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port[0] = value & 0xFF
        self._write()

    def pin(self, pin, value=None):
        pin = self._validate_pin(pin)
        if value is None:
            self._read()
            return (self._port[0] >> pin) & 1
        if value:
            self._port[0] |= 1 << (pin)
        else:
            self._port[0] &= ~(1 << (pin))
        self._write()

    def toggle(self, pin):
        pin = self._validate_pin(pin)
        self._port[0] ^= 1 << (pin)
        self._write()

    def _validate_pin(self, pin):
        # pin valid range 0..7
        if not 0 <= pin <= 7:
            raise ValueError(f"Invalid pin {pin}. Use 0-7.")
        return pin

    def _read(self):
        self._i2c.readfrom_into(self._address, self._port)

    def _write(self):
        self._i2c.writeto(self._address, self._port)
