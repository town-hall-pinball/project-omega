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

log = logging.getLogger("pin.ball")

class Mode(Handler):

    live = False

    def setup(self):
        self.handlers = [
            p.modes["drop_target"],
            p.modes["flippers"],
            p.modes["plunger"],
            p.modes["popper"],
            p.modes["saucer"],
            p.modes["tilt"],
            p.modes["trough"],
            p.modes["slingshots"],
        ]

        self.on("trough_changed", self.is_home)
        self.on("popper_changed", self.is_home)
        self.on("switch_active", self.check_live)

    def dead(self):
        p.modes["drop_target"].disable()
        p.modes["flippers"].disable()
        p.modes["tilt"].disable()
        p.modes["slingshots"].disable()
        p.modes["plunger"].disable()

    def is_home(self):
        in_trough = p.modes["trough"].counter.count()
        in_popper = p.modes["popper"].counter.count()
        if (in_trough == 3 and in_popper == 1) or in_trough == 4:
            p.events.post("home")
            p.notify("mode", "Home")
            self.live = False
            return True
        return False

    def check_live(self, switch):
        if not self.live and "live" in switch.tags:
            p.events.post("live")
            p.notify("mode", "Live")
            self.live = True

    def popper_eject(self, entering=True):
        not_staged = 0 if entering else 1
        if p.modes["popper"].counter.count() == not_staged:
            p.modes["trough"].eject()
        else:
            p.modes["popper"].eject()

    def ball_status(self):
        log.debug("ball status: {} trough, {} popper".format(
                p.modes["trough"].counter.count(),
                p.modes["popper"].counter.count()))






