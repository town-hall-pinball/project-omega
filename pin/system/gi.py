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
from pin.lib.handler import Handler

class Mode(Handler):

    timer = None

    def setup(self):
        self.on("switch", self.switch)
        self.on("data_power_save_timer", self.reset_timer)

    def on_enable(self):
        self.reset_timer()

    def switch(self, *args, **kwargs):
        self.reset_timer()
        self.wake()

    def reset_timer(self):
        self.cancel(self.timer)
        self.timer = self.wait(p.data["power_save_timer"], self.sleep)

    def sleep(self):
        p.events.post("sleep")
        p.notify("mode", "Sleep")
        for gi in p.gi.values():
            # WPC doesn't like patter values for dimming.
            # http://www.pinballcontrollers.com/forum/index.php?topic=452.0
            gi.disable()

    def wake(self):
        p.events.post("wake")
        p.notify("mode", "Wake")
        for gi in p.gi.values():
            gi.enable()

