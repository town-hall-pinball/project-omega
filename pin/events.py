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
import logging

__all__ = ["on", "off", "post", "dispatch", "reset"]

listeners = {}
switch_timings = {}
queue = []
log = logging.getLogger("pin.event")

def on(event, listener):
    """
    Register the `listener` function to be called when an `event` is
    posted. Any additional `*args` and `**kwargs` passed when posting
    the event are also passed to the listener.
    """
    if event not in listeners:
        listeners[event] = []
    listeners[event].append(listener)

def off(event, listener):
    """
    Unregister the `listener` function from being called when an
    `event` is posted. If the `listener` was not previous registered,
    this method does nothing.
    """
    if event in listeners:
        listeners[event].remove(listener)

def post(event, *args, **kwargs):
    """
    Posts a new `event` to the queue. Any additional `*args` and `**kwargs`
    are passed to listeners registered for this event.
    """
    queue.append({
        "event": event,
        "args": args,
        "kwargs": kwargs
    })

def dispatch():
    """
    Dispatches all events and empties the queue.
    """
    while queue:
        item = queue.pop(0)
        log.debug("{}: {} {}".format(item["event"],
                item["args"], item["kwargs"]))
        for listener in listeners.get(item["event"], []):
            listener(*item["args"], **item["kwargs"])
        if item["event"] == "switch":
            handle_switch_event(*item["args"], **item["kwargs"])

def reset():
    """
    Removes all registered listeners and clears the event queue.
    """
    global listeners, queue, switch_timings
    listeners = {}
    queue = []
    switch_timings = {}

def on_switch(name, listener, duration=0, active=True):
    info = switch_timings.get(name, {
        "change_to": None,
        "change_time": 0,
        "last_notice": 0,
        "listeners": []
    })
    info["listeners"] += [{
        "callback": listener,
        "duration": duration,
        "active": active
    }]
    switch_timings[name] = info

def off_switch(name, listener, duration=0, active=True):
    if name not in switch_timings:
        return
    info = switch_timings[name]
    info["listeners"] = [x for x in info["listeners"]
            if x["callback"] != listener]
    if len(info["listeners"]) == 0:
        del switch_timings[name]

def handle_switch_event(switch, active):
    if switch.name not in switch_timings:
        return
    info = switch_timings[switch.name]
    info["change_to"] = active
    info["change_time"] = p.now
    info["last_notice"] = p.now

def tick():
    for info in switch_timings.values():
        for listener in info["listeners"]:
            change_at = info["change_time"] + listener["duration"]
            if (info["last_notice"] < change_at and
                    p.now >= change_at and
                    info["change_to"] == listener["active"]):
                listener["callback"]()
        info["last_notice"] = p.now








