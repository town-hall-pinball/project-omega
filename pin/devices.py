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

devices = {}
switch_numbers = {}
flashers = {}
gi = {}
lamps = {}
switches = {}
coils = {}

class Device(object):

    type = "unknown"

    def __init__(self, name, **config):
        self.name = name
        self.label = config.get("label", name)
        self.device = config["device"]
        self.number = p.platform.devices[self.device]

    def __str__(self):
        return "{}:{}".format(self.type, self.name)


class Driver(Device):

    def __init__(self, name, **config):
        super(Driver, self).__init__(name, **config)

    def enable(self, enabled=True):
        if not enabled:
            self.disable()
        self.log.debug("+ {}".format(self.name))
        p.proc.api.driver_pulse(self.number, 0)

    def disable(self):
        self.log.debug("- {}".format(self.name))
        p.proc.api.driver_disable(self.number)


class Coil(Driver):

    def __init__(self, name, **config):
        super(Coil, self).__init__(name, **config)
        self.type = "coil"
        self.log = logging.getLogger("pin.coil")


class GI(Driver):

    def __init__(self, name, **config):
        super(GI, self).__init__(name, **config)
        self.type = "gi"
        self.log = logging.getLogger("pin.gi")


class Flasher(Driver):

    def __init__(self, name, **config):
        super(Flasher, self).__init__(name, **config)
        self.type = "flasher"
        self.log = logging.getLogger("pin.flasher")


class Lamp(Driver):

    def __init__(self, name, **config):
        super(Lamp, self).__init__(name, **config)
        self.type = "lamp"
        self.log = logging.getLogger("pin.lamp")


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
            raise ValueError("Non-debounced switch")
            events = ["closed_nondebounced", "open_nondebounced"]

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

