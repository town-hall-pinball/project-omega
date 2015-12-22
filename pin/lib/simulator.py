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

from . import p, ui
from .handler import Handler

log = logging.getLogger("pin.sim")

initial = []
rules = {}

class Mode(Handler):

    def setup(self):
        self.balls = set()
        self.free = 0

        p.events.on("data_simulator_enabled", self.update)
        self.on("coil", self.handle_device)
        self.on("switch", self.handle_device)
        self.on("simulator_reset", self.reset_request)
        self.update()

    def update(self):
        if p.data["simulator_enabled"]:
            self.enable()
        else:
            self.disable()

    def on_enable(self):
        log.info("started")
        self.reset()

    def clear(self):
        for switch in set(self.balls):
            switch.deactivate()
            self.balls.remove(switch)

    def reset(self):
        for switch in initial:
            switch.activate()
            self.balls.add(switch)

    def reset_request(self):
        ui.notify("SIM RESET", duration=2.0)
        self.clear()
        self.wait(0, self.reset)

    def on_disable(self):
        log.info("stop")
        self.clear()

    def handle_device(self, device, state=None):
        condition = "{}:{}={}".format(device.type, device.name,
                device.state["schedule"])
        if condition in rules:
            log.debug(condition)
            for rule in rules[condition]:
                self.evaluate_rule(condition, rule)

    def evaluate_rule(self, condition, rule):
        if "disable" in rule:
            rule["disable"].deactivate()
            return
        if "enable" in rule:
            rule["enable"].activate()
            return

        source = rule.get("from")
        target = rule.get("to")

        #log.debug("from {}, to {}, free {}".format(source, target, self.free))

        # Is a free ball the source? Is one available?
        if not source and self.free == 0:
            log.warn("No free balls on the playfield to acquire")
            return

        # Is the ball actually at the source location?
        if source and source not in self.balls:
            # Free ball on playfield?
            #if self.free > 0:
            #    source = None # Grab from playfield
            #else:
            #    log.warn("Ball not at {} and no free ball to acquire".format(
            #            source.name))
            return

        # Is the target location blocked by a ball?
        if target in self.balls:
            return

        # If playfield to playfield, ignore
        if not source and not target:
            return

        source_name = source.name if source else "playfield"
        source_label = source.label if source else "Playfield"
        target_name = target.name if target else "playfield"
        target_label = target.label if target else "Playfield"

        log.debug("{} to {}".format(source_name, target_name))
        p.events.post("simulate", source, target)
        p.notify("simulate", "{} to {}".format(source_label, target_label))

        if source:
            self.balls.remove(source)
            source.deactivate()
            p.proc.process()
            p.events.dispatch()
        else:
            self.free -= 1

        if target:
            self.balls.add(target)
            if not target.active:
                target.activate()
            p.proc.process()
            p.events.dispatch()
        else:
            self.free += 1

        switch_hit = rule.get("hit")
        if switch_hit:
            p.timers.wait(0.05, switch_hit.activate)
            p.timers.wait(0.10, switch_hit.deactivate)



