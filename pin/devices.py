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

import p

class Device(object):

    def __init__(self, name, **config):
        self.name = name
        self.label = config.get("label", name)
        self.device = config["device"]


class Driver(Device):

    def __init__(self, name, **config):
        super(Driver, self).__init__(name, **config)


class Coil(Driver):

    def __init__(self, name, **config):
        super(Coil, self).__init__(name, **config)
        self.number = p.platform["map"]["coils"][self.device]


class Switch(Device):

    def __init__(self, name, **config):
        super(Switch, self).__init__(name, **config)
        self.number = p.platform["map"]["switches"][self.device]
        self.debounce = self.number < 192

    def enable(self, enable=True):
        if switch.debounce:
            events = ["closed_debounced", "open_debounced"]
        else:
            events = ["closed_nondebounced", "open_nondebounced"]

        for event in events:
            p.proc.switch_update_rule(switch.number, event, {
                "notifyHost": enable,
                "reloadActive": False
            }, [], False)

    def disable(self):
        self.enable(False)


def add_switches(configs):
    for name, config in configs.items():
        p.switches[name] = Switch(name, **config)

def add_coils(configs):
    for name, config in configs.items():
        p.coils[name] = Coil(name, **config)

