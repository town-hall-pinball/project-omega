# Copyright (c) 2014 - 2016 townhallpinball.org
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
from pin.lib.util import BallCounter, Eject
from pin.lib.handler import Handler

class Mode(Handler):

    def setup(self):
        self.on_switch("shooter_lane", self.shooter_lane, 0.25)
        self.coil = Eject(self, p.coils["trough"])
        self.counter = BallCounter(self, "trough", [
            p.switches["trough"],
            p.switches["trough_2"],
            p.switches["trough_3"],
            p.switches["trough_4"]
        ])
        self.on("switch_trough_4", self.drain)

    def eject(self):
        self.coil.eject()

    def shooter_lane(self):
        self.coil.success()

    def drain(self):
        p.notify("game", "Drain")
        p.events.post("drain")


