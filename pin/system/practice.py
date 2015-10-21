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

from pin.lib import p, ui
from pin.lib.handler import Handler
from pin.machine.game import Game as BaseGame

class Mode(BaseGame):

    def setup(self):
        super(Mode, self).setup()
        self.max_players = 1
        self.max_time = 0
        self.display = ui.Panel()
        self.time = ui.Text("0:00", font="c128_16")
        self.display.add((self.time,))
        self.ticker = None
        self.start_time = None
        self.on("live_ball", self.live_ball_check)

    def on_enable(self):
        super(Mode, self).on_enable()
        p.captures["trough"].eject()
        self.max_time = p.data["practice_timer"]
        self.update_time()

    def on_disable(self):
        p.timers.cancel(self.ticker)

    def live_ball_check(self):
        if not self.start_time:
            self.ticker = p.timers.tick(self.update_time)
            self.start_time = p.now

    def update_time(self):
        elapsed = 0
        if self.start_time:
            elapsed = p.now - self.start_time
        remaining = self.max_time - elapsed
        if remaining < 0:
            remaining = 0
        minutes = int(remaining / 60)
        seconds = int(remaining % 60)
        self.time.show("{}:{:02d}".format(minutes, seconds))


    def live_ball(self):
        super(Mode, self).live_ball()
        self.auto_launch = True



