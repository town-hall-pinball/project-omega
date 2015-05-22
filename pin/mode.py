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

import p

class BaseMode(object):

    def __init__(self):
        self.key = None
        self.name = None
        self.setup()
        self.listeners = {}
        self.enabled = False
        p.modes[self.key] = self

    def setup(self):
        pass

    def on(self, event, listener):
        if event in self.listeners:
            raise ValueError("Listener already registered for {}"
                    .format(event))
        self.listeners[event] = listener
        if self.active:
            p.events.on(event, listener)

    def off(self, event, listener):
        self.listeners.remove(event)
        p.events.off(event, listener)

    def enable(self):
        if self.enabled:
            return
        for event, listener in self.listeners.items():
            p.events.on(event, listener)
        self.start()

    def start(self):
        pass

    def disable(self):
        if not self.enabled:
            return
        for event, listener in self.listeners.items():
            p.events.off(event, listener)
        self.stop()

    def stop(self):
        pass

    def render(self, frame):
        pass




