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
from pin.lib.util import BallCounter, Eject
from pin.lib.handler import Handler

class Mode(Handler):

    balls = 0
    entering = False
    exiting = False

    # TODO: During multiball it is probably not possible to track enter/exit
    # states of the ball. Might need to simply keep firing the popper until
    # the queue is clear?
    multi = False

    def setup(self):
        self.on("switch_subway_center", self.subway)
        self.on("switch_subway_left", self.subway)
        self.on("switch_popper_2", self.enter)
        self.on("switch_return_right", self.exit)
        self.coil = Eject(self, p.coils["popper"])
        self.counter = BallCounter(self, "popper", [
            p.switches["popper"],
            p.switches["popper_2"]
        ])
        self.on("popper_changed", self.count_changed)

    def on_enable(self):
        self.count_changed()
        self.reset()

    def on_disable(self):
        self.reset()
        p.flashers["popper"].disable()

    def reset(self):
        self.entering = False
        self.exiting = False
        self.multi = False

    def subway(self):
        if not self.entering:
            self.entering = True
            p.events.post("entering_popper")

    def enter(self):
        self.entering = False
        p.events.post("enter_popper")

    def eject(self):
        p.flashers["popper"].patter(100, 127)
        self.wait(1.0, self.pop)

    def pop(self):
        p.flashers["popper"].disable()
        self.coil.eject()
        self.exiting = True

    def exit(self):
        if self.exiting:
            self.exiting = False
            p.events.post("exit_popper")
            self.coil.success()

    def count_changed(self):
        self.balls = self.counter.balls


