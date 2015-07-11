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
from pin import util
from pin.handler import Handler

total = 0
captures = {}
search_sequence = []

class Capture(Handler):

    def __init__(self, name, switches, coil, verify, staged=0):
        self.name = name
        self.switches = switches
        self.coil = coil
        self.verify = verify
        self.staged = staged

    def balls(self):
        amount = 0
        for switch in self.switches:
            if switch.active:
                amount += 1
        return amount


def add_captures(configs):
    for name, config in configs.items():
        if name in captures:
            raise ValueError("Duplicate ball capture: {}".format(name))
        captures[name] = Capture(name, **config)



class Mode(Handler):
    pass


def trough_count():
    amount = 0
    for capture in captures:
        balls = capture.balls()
        if captures.name == "trough":
            amount += balls
        if captures.staged:
            amount += max(balls, captures.staged)
    return amount

def trough_ready():
    return trough_ready == total





