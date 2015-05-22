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

__all__ = ["Events"]

class Events(object):
    """
    Event queue.

    The system-wide event queue is found at :data:`p.events`
    """

    listeners = None
    queue = []
    log = None

    def __init__(self):
        self.listeners = {}
        self.queue = []
        self.log = logging.getLogger("pin.event")

    def on(self, event, listener):
        """
        Register the `listener` function to be called when an `event` is
        posted. Any additional `*args` and `**kwargs` passed when posting
        the event are also passed to the listener.
        """
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event] += [listener]

    def off(self, event, listener):
        """
        Unregister the `listener` function from being called when an
        `event` is posted. If the `listener` was not previous registered,
        this method does nothing.
        """
        if event in self.listeners:
            self.listeners[event].remove(listener)

    def post(self, event, *args, **kwargs):
        """
        Posts a new `event` to the queue. Any additional `*args` and `**kwargs`
        are passed to listeners registered for this event.
        """
        self.queue += [{
            "event": event,
            "args": args,
            "kwargs": kwargs
        }]

    def dispatch(self):
        """
        Dispatches all events and empties the queue.
        """
        while self.queue:
            item = self.queue.pop(0)
            self.log.debug("{}: {} {}".format(item["event"],
                    item["args"], item["kwargs"]))
            for listener in self.listeners.get(item["event"], []):
                listener(*item["args"], **item["kwargs"])


