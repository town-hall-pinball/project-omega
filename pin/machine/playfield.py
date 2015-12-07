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

from pin.lib import p, devices
from pin.lib.handler import Handler

log = logging.getLogger("pin")

class Mode(Handler):

    live = False

    def setup(self):
        self.drop_target = p.modes["drop_target"]
        self.flippers = p.modes["flippers"]
        self.plunger = p.modes["plunger"]
        self.popper = p.modes["popper"]
        self.saucer = p.modes["saucer"]
        self.slingshots = p.modes["slingshots"]
        self.trough = p.modes["trough"]

        self.handlers = [
            self.drop_target,
            self.flippers,
            self.plunger,
            self.popper,
            self.saucer,
            self.trough,
            self.slingshots,
        ]

        self.on("trough_changed", self.is_home)
        self.on("popper_changed", self.is_home)
        self.on("switch_active", self.check_live)

    def is_home(self):
        in_trough = self.trough.counter.count()
        in_popper = self.popper.counter.count()
        if (in_trough == 3 and in_popper == 1) or in_trough == 4:
            p.events.post("home")
            self.live = False
            return True
        return False

    def check_live(self, switch):
        #log.debug("live check on {}".format(switch.name))
        if not self.live and "live" in switch.tags:
            #log.debug("live on " + switch.name)
            p.events.post("live")
            self.live = True

    def popper_eject(self, entering=True):
        not_staged = 0 if entering else 1
        if p.modes["popper"].counter.count() == not_staged:
            p.modes["trough"].eject()
        else:
            p.modes["popper"].eject()

    def ball_status(self):
        log.debug("ball status: {} trough, {} popper".format(
                self.trough.counter.count(),
                self.popper.counter.count()))






