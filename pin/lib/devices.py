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

from . import p

log = {
    "coil": logging.getLogger("pin.coil"),
    "flasher": logging.getLogger("pin.flasher"),
    "gi": logging.getLogger("pin.gi"),
    "lamp": logging.getLogger("pin.lamp"),
    "switch": logging.getLogger("pin.switch")
}

devices = {}
switch_numbers = {}
switch_devices = {}
flashers = {}
flippers = {}
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

    state = None

    def __init__(self, name, **config):
        self.name = name
        self.label = config.get("label", name)
        self.device = config["device"]
        self.tags = config.get("tags", [])
        self.number = p.platform.devices[self.device]
        self.state = { "schedule": "disable" }

    def __str__(self):
        return "{}:{}".format(self.type, self.name)


class Driver(Device):
    """
    A :py:class:`Device` in the pinball machine that can be driven by software.
    """

    def __init__(self, name, **config):
        super(Driver, self).__init__(name, **config)
        self.default_pulse_length = config.get("default_pulse_length", 30)
        self.default_patter_length = config.get("default_patter_length", 127)

    def enable(self, enabled=True, show=False):
        """
        Enables this device for an indefinate amount of time. Can be
        disabled by specifying `False` for `enabled`
        """
        if not enabled:
            self.disable(show)
            return
        state = { "schedule": "enable", "show": show }
        if self.state == state:
            return
        self.state = state
        if not show:
            log[self.type].debug("+ {}".format(self.name))
        p.proc.api.driver_pulse(self.number, 0)
        p.events.post(self.type, self)

    def disable(self, show=False):
        """
        Disables this device.
        """
        state = { "schedule": "disable", "show": show }
        if self.state == state:
            return
        self.state = state
        if not show:
            log[self.type].debug("- {}".format(self.name))
        p.proc.api.driver_disable(self.number)
        p.events.post(self.type, self)

    def is_active(self):
        return self.state["schedule"] != "disable"

    def pulse(self, pulse_length=None, show=False):
        """
        Enables this devices for `pulse_length` milliseconds. If `pulse_length`
        is not provided, it defaults to the configured `default_pulse_length`
        """
        suffix = ""
        if pulse_length is None:
            pulse_length = self.default_pulse_length
        else:
            suffix = "for {}ms".format(pulse_length)
        self.state = { "schedule": "pulse", "duration": pulse_length,
                "show": show }

        log[self.type].debug("+ {} {}".format(self.name, suffix))
        p.proc.api.driver_pulse(self.number, pulse_length)
        p.events.trigger(self.type, self)
        p.events.trigger("{}_{}".format(self.type, self.name))
        self.state = { "schedule": "disable" }

    def patter(self, on=None, off=None):
        """
        Repeats a sequence when the device is enabled for `on` milliseconds
        and disabled for `off` milliseconds. Maximum `on` and `off` times are
        127ms.
        """
        on = on or self.default_patter_length
        off = off or self.default_patter_length
        state = { "schedule": "patter", "on": on, "off": off }
        if self.state == state:
            return
        self.state = state
        log[self.type].debug("+ {} patter on={}, off={}".format(self.name,
                on, off))
        p.proc.api.driver_patter(self.number, on, off, 0, 0)
        p.events.post(self.type, self)
        p.events.post("{}_{}".format(self.type, self.name))


class Coil(Driver):
    """
    :py:class:`Driver` for a coil/solenoid. Each coil is normally configured
    in :py:mod:`pin.machine.coils`

    State changes are logged to `pin.coil`
    """

    def __init__(self, name, **config):
        super(Coil, self).__init__(name, **config)
        self.type = "coil"
        self.auto_switch_name = None

    def auto_pulse(self, switch, pulse_length=None):
        if self.auto_switch_name:
            raise ValueError("Coil already in auto mode")
        self.auto_switch_name = switch.name
        pulse_length = pulse_length or self.default_pulse_length

        coil_state = p.proc.api.driver_get_state(self.number)
        on_drivers = [
            p.proc.api.driver_state_pulse(coil_state, pulse_length),
        ]
        event = "open_debounced" if switch.opto else "closed_debounced"
        p.proc.api.switch_update_rule(switch.number, event, {
            "notifyHost": False,
            "reloadActive": False
        }, on_drivers, True)

    def auto_patter(self, switch, on=None, off=None):
        if self.auto_switch_name:
            raise ValueError("Coil already in auto mode")
        self.auto_switch_name = switch.name
        on = on or self.default_patter_length
        off = off or self.default_patter_length

        coil_state = p.proc.api.driver_get_state(self.number)
        on_drivers = [
            p.proc.api.driver_state_patter(coil_state, on, off, 0, 0),
        ]
        event = "open_debounced" if switch.opto else "closed_debounced"
        p.proc.api.switch_update_rule(switch.number, event, {
            "notifyHost": False,
            "reloadActive": False
        }, on_drivers, True)

    def auto_cancel(self):
        if not self.auto_switch_name:
            return
        switch = p.switches[self.auto_switch_name]
        event = ("open_debounced" if switch.opto else "closed_debounced")
        p.proc.api.switch_update_rule(switch.number, event, {
            "notifyHost": False,
            "reloadActive": False
        }, [], False)
        self.auto_switch_name = None


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

    def activate(self):
        if not self.active:
            event = p.proc.SWITCH_OPENED if self.opto else p.proc.SWITCH_CLOSED
            p.proc.artificial_events += [{"type": event, "value": self.number}]

    def deactivate(self):
        if self.active:
            event = p.proc.SWITCH_CLOSED if self.opto else p.proc.SWITCH_OPENED
            p.proc.artificial_events += [{"type": event, "value": self.number}]

    def is_closed(self):
        return self.active if not self.opto else not self.active

    def is_opened(self):
        return not self.is_closed()


class Flipper(Device):

    pulse_time = 30

    def __init__(self, name, **config):
        super(Flipper, self).__init__(name, **config)
        self.hold_device = config["hold_device"]
        self.hold_number = p.platform.devices[self.hold_device]
        self.switch_name = config["switch"]
        self.auto_switch_name = None

    def auto_pulse(self, enable=True):
        if not enable:
            self.disable()
            return
        main_coil_state = p.proc.api.driver_get_state(self.number)
        hold_coil_state = p.proc.api.driver_get_state(self.hold_number)

        # From: https://github.com/preble/pyprocgame/blob/master/procgame/game/game.py#L417-L459
        on_drivers = [
            p.proc.api.driver_state_pulse(main_coil_state, self.pulse_time),
            p.proc.api.driver_state_pulse(hold_coil_state, 0)
        ]
        switch = p.switches[self.switch_name]
        p.proc.api.switch_update_rule(switch.number,
            "closed_nondebounced", {
                "notifyHost": False,
                "reloadActive": False
            }, on_drivers, True)

        off_drivers = [
            p.proc.api.driver_state_disable(hold_coil_state)
        ]
        p.proc.api.switch_update_rule(switch.number,
            "open_nondebounced", {
                "notifyHost": False,
                "reloadActive": False
            }, off_drivers, True)
        self.auto_switch_name = self.switch_name

    def auto_cancel(self):
        switch = p.switches[self.switch_name]
        p.proc.api.switch_update_rule(switch.number,
            "closed_nondebounced", {
                "notifyHost": False,
                "reloadActive": False
            }, [], False)
        p.proc.api.switch_update_rule(switch.number,
            "open_nondebounced", {
                "notifyHost": False,
                "reloadActive": False
            }, [], False)
        p.proc.api.driver_disable(self.number)
        p.proc.api.driver_disable(self.hold_number)
        self.auto_switch_name = None


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

def add_flippers(configs):
    add(flippers, Flipper, configs)

def reset():
    coils.clear()
    devices.clear()
    flashers.clear()
    flippers.clear()
    gi.clear()
    lamps.clear()
    switches.clear()
    switch_numbers.clear()

