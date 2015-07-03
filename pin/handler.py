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
        self.enabled = False
        self.suspended = False
        self.handlers = []
        self.renderer = None
        self.display = None
        self.setup()

    def setup(self):
        pass

    def on(self, event, listener):
        if event in self.listeners:
            raise ValueError("Listener already registered for {}"
                    .format(event))
        self.listeners[event] = listener
        if self.enabled:
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


    def enable(self, enabled=True, transition=None):
        if not enabled:
            self.disable()
            return
        if self.enabled:
            return
        log.debug("{} enabled".format(self.name))
        self.enabled = True
        if self.display:
            p.dmd.add(self.display, transition)
        self.register()
        self.on_enable()

    def on_enable(self):
        pass

    def disable(self):
        if not self.enabled:
            return
        log.debug("{} disabled".format(self.name))
        self.enabled = False
        if self.display:
            p.dmd.remove(self.display)
        self.unregister()
        for handler in self.handlers:
            handler.disable()
        self.on_disable()

    def on_disable(self):
        pass

    def suspend(self):
        log.debug("{} suspended".format(self.name))
        self.suspended = True
        #self.unregister()
        if self.display:
            self.display.render_suspend()
        self.on_suspend()

    def on_suspend(self):
        pass

    def resume(self):
        self.suspended = False
        if not self.enabled:
            return
        log.debug("{} resumed".format(self.name))
        #self.register()
        if self.display:
            self.display.render_start()
        self.on_resume()

    def on_resume(self):
        pass

    def register(self):
        #for handler in self.handlers:
        #    handler.enable()
        for event, listener in self.listeners.items():
            p.events.on(event, listener)

    def unregister(self):
        for handler in self.handlers:
            self.disable()
        for event, listener in self.listeners.items():
            p.events.off(event, listener)
        for ident in self.timers:
            p.timers.clear(ident)






