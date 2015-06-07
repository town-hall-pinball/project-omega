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

from pin.handler import Handler

log = logging.getLogger("pin.shows")

class Show(Handler):

    running = False
    index = 0

    def __init__(self, name, timings, repeat=False):
        super(Show, self).__init__(name)
        self.timings = timings
        if repeat == True:
            self.repeat = -1
        elif repeat == False:
            self.repeat = 0
        else:
            self.repeat = repeat
        self.timer = None

    def start(self):
        if not self.running:
            self.running = True
            log.debug("{} started".format(self.name))
            self.started()
            self.next()

    def reset(self):
        self.index = 0
        self.start()

    def started(self):
        pass

    def stop(self):
        if self.running:
            self.running = False
            log.debug("{} stopped".format(self.name))
            self.cancel(self.timer)
            self.timer = None
            self.stopped()

    def stopped(self):
        pass

    def next(self):
        self.cancel(self.timer)
        if self.index == len(self.timings):
            if self.repeat != 0:
                self.index = 0
                if self.repeat > 0:
                    self.repeat -= 1
            else:
                self.stop()
                return
        self.action()
        self.timer = self.wait(self.timings[self.index], self.next)
        self.index += 1


    def action(self):
        pass




