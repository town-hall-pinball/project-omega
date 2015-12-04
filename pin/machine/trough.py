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

from pin.lib import p
from pin.lib.util import Eject
from pin.lib.handler import Handler

class Mode(Handler):

    live = False

    def setup(self):
        self.on_switch("shooter_lane", self.shooter_lane, 0.25)
        self.trough = Eject(self, p.coils["trough"])

    def on_enable(self):
        p.notify("mode", "Trough enabled")
        self.live = False

    def on_disable(self):
        p.notify("mode", "Trough disabled")

    def feed(self):
        p.notify("mode", "Trough feed")
        self.trough.eject()

    def shooter_lane(self):
        if not self.live:
            p.notify("mode", "Live ball")
            p.events.trigger("live_ball")
        self.live = True
        self.trough.success()

