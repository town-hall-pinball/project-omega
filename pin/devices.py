# Copyright (c) 2014 - 2015 townhallpinball.org
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import logging

import p

log = {
    "coil": logging.getLogger("pin.coil"),
    "flasher": logging.getLogger("pin.flasher"),
    "gi": logging.getLogger("pin.gi"),
    "lamp": logging.getLogger("pin.lamp"),
    "switch": logging.getLogger("pin.switch")
}

devices = {}
switch_numbers = {}
flashers = {}
gi = {}
lamps = {}
switches = {}
coils = {}

class Device(object):
    """
    A device in the pinball machine such as a switch, coil, lamp, etc.
    """

    name = None
    """
    Name of the device used as an identifier (e.g., `auto_plunger`)
    """

    label = None
    """
    Descriptive name of the device (e.g., `Auto Plunger`)
    """

    device = None
    """
    The string representation of this device by lookup in the owner's manual.
    """

    number = None
    """
    Address number of the device used by the P-ROC
    """

    type = "unknown"
    """
    Descriptive type of the device, such as "switch" or "coil"
    """

    state = { "schedule": "disable" }

    def __init__(self, name, **config):
        self.name = name
        self.label = config.get("label", name)
        self.device = config["device"]
        self.number = p.platform.devices[self.device]

    def __str__(self):
        return "{}:{}".format(self.type, self.name)


class Driver(Device):
    """
    A :py:class:`Device` in the pinball machine that can be driven by software.
    """

    def __init__(self, name, **config):
        super(Driver, self).__init__(name, **config)

    def enable(self, enabled=True):
        """
        Enables this device for an indefinate amount of time. Can be
        disabled by specifying `False` for `enabled`
        """
        if not enabled:
            self.disable()
        log[self.type].debug("+ {}".format(self.name))
        p.proc.api.driver_pulse(self.number, 0)

    def disable(self):
        """
        Disables this device.
        """
        log[self.type].debug("- {}".format(self.name))
        p.proc.api.driver_disable(self.number)


class Coil(Driver):
    """
    :py:class:`Driver` for a coil/solenoid. Each coil is normally configured
    in :py:mod:`pin.machine.coils`

    State changes are logged to `pin.coil`
    """

    def __init__(self, name, **config):
        super(Coil, self).__init__(name, **config)
        self.type = "coil"


class GI(Driver):

    def __init__(self, name, **config):
        super(GI, self).__init__(name, **config)
        self.type = "gi"


class Flasher(Driver):

    def __init__(self, name, **config):
        super(Flasher, self).__init__(name, **config)
        self.type = "flasher"


class Lamp(Driver):

    def __init__(self, name, **config):
        super(Lamp, self).__init__(name, **config)
        self.type = "lamp"


class Switch(Device):

    def __init__(self, name, **config):
        super(Switch, self).__init__(name, **config)
        self.type = "switch"
        self.debounce = self.number < 192
        self.opto = config.get("opto", False)
        self.active = False

    def enable(self, enable=True):
        if self.debounce:
            events = ["closed_debounced", "open_debounced"]
        else:
            # Don't worry about this now
            raise ValueError("Non-debounced switch") # pragma: no cover
            #events = ["closed_nondebounced", "open_nondebounced"]

        for event in events:
            p.proc.api.switch_update_rule(self.number, event, {
                "notifyHost": enable,
                "reloadActive": False
            }, [], False)

    def disable(self):
        self.enable(False)


def add(collection, clazz, configs):
    for name, config in configs.items():
        obj = clazz(name, **config)
        if name in collection:
            raise ValueError("Duplicate {}: {}".format(obj.type, name))
        if obj.device in devices:
            other = devices[obj.device]
            raise ValueError("{} also maps to {}".format(obj, other))

        if clazz == Switch:
            if obj.number in switch_numbers:
                other = switch_numbers[obj.number]
                raise ValueError("Duplicate address number {} for {} and {}"
                        .format(obj.number, obj, other))
            switch_numbers[obj.number] = obj

        devices[obj.device] = obj
        collection[name] = obj

def add_switches(configs):
    add(switches, Switch, configs)

def add_coils(configs):
    add(coils, Coil, configs)

def add_gi(configs):
    add(gi, GI, configs)

def add_lamps(configs):
    add(lamps, Lamp, configs)

def add_flashers(configs):
    add(flashers, Flasher, configs)

def reset():
    coils.clear()
    devices.clear()
    flashers.clear()
    gi.clear()
    lamps.clear()
    switches.clear()
    switch_numbers.clear()

