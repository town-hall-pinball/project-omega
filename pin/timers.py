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

from pin import util

counter = util.Counter()
active = {}
tickers = {}

def set(duration, callback):
    """
    Register `callback` to be invoked one time after `duration` seconds
    have elapsed. Returns an identifier that can be used to cancel this
    registration using :meth:`clear`.
    """
    ident = counter.next()
    active[ident] = {
        "duration": duration,
        "end": p.now + duration,
        "callback": callback
    }
    return ident

def tick(callback):
    """
    Register `callback` to be invoked each time the main loop runs. Returns
    an identifier that can be used to cancel this registration using
    :meth:`clear`.
    """
    ident = counter.next()
    tickers[ident] = callback
    return ident

def clear(ident):
    """
    Unregister a callback that was assigned with the identifier, `ident`
    """
    if ident in active:
        del active[ident]
    if ident in tickers:
        del tickers[ident]

def service():
    """
    Service all active timers.
    """
    if len(active) > 0:
        for ident, timer in active.items():
            if p.now > timer["end"] and ident in active:
                del active[ident]
                timer["callback"]()
    for ticker in tickers.values():
        ticker()


def process():
    """
    Called by the main processor on each loop to service all timers.
    """
    service()
