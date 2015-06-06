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
import p

log = logging.getLogger("pin.handler")

class Handler(object):

    frame = None

    def __init__(self, name):
        self.name = name
        self.listeners = {}
        self.timers = set()
        self.active = False
        self.handlers = []
        self.renderer = None
        self.setup()

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

    def wait(self, duration, callback):
        def expire(expired):
            self.timers.remove(expired)
            callback()
        ident = p.timers.set(duration, expire, with_ident=True)
        self.timers.add(ident)
        return ident

    def cancel(self, ident):
        if ident:
            if ident in self.timers:
                self.timers.remove(ident)
            p.timers.clear(ident)


    def enable(self, enabled=True):
        if not enabled:
            self.disable()
            return
        if self.active:
            return
        self.active = True
        for handler in self.handlers:
            handler.enable()
        for event, listener in self.listeners.items():
            p.events.on(event, listener)
        self.enabled()
        log.debug("{} enabled".format(self.name))

    def enabled(self):
        pass

    def disable(self):
        if not self.active:
            return
        self.active = False
        for handler in self.handlers:
            self.disable()
        for event, listener in self.listeners.items():
            p.events.off(event, listener)
        for ident in self.timers:
            p.timers.clear(ident)
        self.disabled()
        log.debug("{} disabled".format(self.name))

    def disabled(self):
        pass

    def render(self, frame):
        if not self.active:
            return
        for handler in self.handlers:
            handler.render(frame)
        if self.renderer:
            self.renderer.render(frame)

    def render_started(self):
        pass

    def render_stopped(self):
        pass

    def render_restarted(self):
        pass





