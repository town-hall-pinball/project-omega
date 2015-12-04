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

class BallCounter(object):

    settle_time = 0.25
    balls = 0

    def __init__(self, handler, name, switches):
        self.name = name
        self.switches = switches
        for switch in self.switches:
            handler.on_switch(switch.name, self.check_count,
                    self.settle_time, active=True)
            handler.on_switch(switch.name, self.check_count,
                    self.settle_time, active=False)
        self.balls = self.count()

    def count(self):
        count = 0
        for switch in self.switches:
            if switch.active:
                count += 1
        return count

    def check_count(self):
        previous = self.balls
        current = self.count()
        if previous != current:
            self.balls = current
            p.events.post("{}_changed", current)


