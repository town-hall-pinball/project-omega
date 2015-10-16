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

import collections
import logging

from pin.lib import p
from pin.lib.handler import Handler

log = logging.getLogger("pin.shot")
rule_set = {}

class Mode(Handler):

    history = collections.deque(maxlen=5)

    def setup(self):
        p.events.on("playfield_enable", self.enable)
        p.events.on("playfield_disable", self.disable)
        self.on("switch_active", self.switch_active)

    def switch_active(self, switch=None):
        log.warn("****** GOT IT: " + switch.name)
        if not "user" in switch.tags:
            self.history.appendleft(switch)
        for shot_name, rules in rule_set.items():
            self.evaluate_shot(shot_name, rules)

    def evaluate_shot(self, shot_name, rules):
        for rule, switch in zip(rules, self.history):
            if "eq" in rule and rule["eq"].name != switch.name:
                return
            elif "neq" in rule and rule["neq"].name == switch.name:
                return
            elif "eq" not in rule and "neq" not in rule:
                raise ValueError("Invalid rule in {}: {}".format(shot_name,
                        rule))
        log.debug("+ {}".format(shot_name))
        p.events.trigger(shot_name)

    def on_disable(self):
        self.history.clear()
