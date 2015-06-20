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
from pin import devices
from pin.virtual import dmd as virtual_dmd

SWITCH_CLOSED = 1
SWITCH_OPENED = 2
SWITCH_CLOSED_NOT_DEBOUNCED = 3
SWITCH_OPENED_NOT_DEBOUNCED = 4
DMD_READY = 5

api = None
artificial_events = []
dmd_buffer = None
log =  logging.getLogger("pin.proc")
switch_log = logging.getLogger("pin.switch")

def init():
    global dmd_buffer
    api.reset(1)
    for switch in p.switches.values():
        switch.enable()
    dmd_buffer = create_buffer()

def create_buffer():
    import pinproc
    return pinproc.DMDBuffer(p.dmd.width, p.dmd.height)

def switch_active(switch):
    p.events.post("switch_{}".format(switch.name))
    p.events.post("switch_{}_active".format(switch.name))
    p.events.post("switch_active", switch)
    p.events.post("switch", switch, True)
    switch.active = True
    switch_log.debug("+ {}".format(switch.name))

def switch_inactive(switch):
    p.events.post("switch_{}_inactive".format(switch.name))
    p.events.post("switch_inactive", switch)
    p.events.post("switch", switch, False)
    switch.active = False
    switch_log.debug("- {}".format(switch.name))

def handle_switch(event):
    number = event["value"]
    switch = devices.switch_numbers[number]
    if event["type"] == SWITCH_OPENED:
        switch_active(switch) if switch.opto else switch_inactive(switch)
    else: #SWITCH_CLOSED
        switch_inactive(switch) if switch.opto else switch_active(switch)

def refresh_dmd(frame):
    dots = p.dmd.create_dots(frame)
    for x in xrange(p.dmd.width):
        for y in xrange(p.dmd.height):
            v = (dots[x, y] >> 4) & 0xf
            dmd_buffer.set_dot(x, y, v)
    api.dmd_draw(dmd_buffer)

def handle_events(events):
    for event in events:
        if event["type"] == DMD_READY:
            frame = p.dmd.render()
            refresh_dmd(frame)
            if p.options["virtual"]:
                virtual_dmd.update(frame)
        elif event["type"] in (SWITCH_OPENED, SWITCH_CLOSED):
            handle_switch(event)
        else:
            log.error("Unsupported event type: {}".format(event["type"]))

def process():
    handle_events(api.get_events())
    handle_events(artificial_events)
    api.watchdog_tickle()
    api.flush()
    artificial_events[:] = []

def reset():
    artificial_events[:] = []


