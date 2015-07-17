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

import itertools
import logging

import p
from pin.handler import Handler

log = logging.getLogger("pin.shows")

class Show(Handler):

    running = False
    index = 0
    count = 0

    def __init__(self, name, timings, repeat=False, action=None, callback=None):
        super(Show, self).__init__(name)
        self.timings = timings
        if repeat == True:
            self.repeat = -1
        elif repeat == False:
            self.repeat = 0
        else:
            self.repeat = repeat
        self.original_repeat = self.repeat
        self.timer = None
        self.fn_action = action
        self.fn_finished = callback

    def start(self):
        if not self.running:
            log.debug("{} started".format(self.name))
            self._start()

    def _start(self):
        self.running = True
        self.on_start()
        self.next()

    def restart(self):
        self.index = 0
        self.repeat = self.original_repeat
        log.debug("{} restarted".format(self.name))
        self._start()

    def on_start(self):
        pass

    def stop(self):
        if self.running:
            self.running = False
            log.debug("{} stopped".format(self.name))
            self.cancel(self.timer)
            self.timer = None
            self.on_stop()

    def on_stop(self):
        pass

    def next(self):
        self.cancel(self.timer)
        if not self.running:
            return
        if self.index == len(self.timings):
            if self.repeat != 0:
                self.index = 0
                if self.repeat > 0:
                    self.repeat -= 1
            else:
                self.stop()
                if self.fn_finished:
                    self.fn_finished()
                return
        use_callback = False
        if self.fn_action:
            self.fn_action()
        else:
            use_callback = self.timings[self.index] is None
            self.action(use_callback)
        if not use_callback:
            self.timer = self.wait(self.timings[self.index], self.next)
        self.index += 1
        self.count += 1

    def action(self, use_callback=False):
        pass



class LightShow(Show):

    def __init__(self, name, interval, lights):
        length = 0
        for sequence in lights.values():
            length = max(length, len(sequence))
        super(LightShow, self).__init__(name, [interval] * length, True)
        self.lights = lights

    def stop(self):
        super(LightShow, self).stop()
        for light in self.lights:
            p.lamps[light].disable(show=True)

    def action(self, use_callback=False):
        for light, sequence in self.lights.items():
            index = self.count % len(sequence)
            if sequence[index]:
                p.lamps[light].enable(show=True)
            else:
                p.lamps[light].disable(show=True)



