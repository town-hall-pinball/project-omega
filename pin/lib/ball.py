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

import collections
import logging

from . import p, util
from .handler import Handler

log = logging.getLogger("pin.ball")
shot_log = logging.getLogger("pin.shot")

total = 0
captures = {}
shots = {}
search_sequence = []
search_interval = 0.25

max_eject_attempts = 20

class Capture(Handler):

    def __init__(self, name, switches, coil, verify=None, staged=0):
        self.switches = switches
        self.coil = coil
        self.verify = verify or {}
        self.verify["type"] = self.verify.get("type", "none")
        self.verify["time"] = self.verify.get("time", 1.0)
        self.verify["retry_time"] = self.verify.get("retry_time", 3.0)
        self.staged = staged
        super(Capture, self).__init__(name)

    def setup(self):
        self.ejecting = False
        self.eject_attempts = 0
        self.timer = None
        self.jammed = False
        if self.verify["type"] == "success":
            event_name = "switch_{}".format(self.verify["switch"].name)
            self.on(event_name, self.check_success)

    def balls(self):
        amount = 0
        for switch in self.switches:
            if switch.active:
                amount += 1
        return amount

    def eject(self, retry=False):
        log.debug("ejecting {}".format(self.name))
        self.ejecting = True
        self.jammed = False
        self.coil.pulse()
        self.eject_attempts += 1
        time = self.verify["retry_time"] if retry else self.verify["time"]
        self.timer = self.wait(time, self.check_timeout)

    def check_success(self):
        if self.ejecting:
            self.confirm_eject()

    def retry(self):
        self.cancel(self.timer)
        if self.eject_attempts >= max_eject_attempts:
            self.give_up()
        else:
            self.eject(retry=True)

    def confirm_eject(self):
        self.cancel(self.timer)
        self.ejecting = False
        self.eject_attempts = 0

    def give_up(self):
        self.ejecting = False
        self.eject_attempts = 0
        self.jammed = True

    def check_timeout(self):
        if self.ejecting:
            if self.verify["type"] == "success":
                self.retry()
            elif ( self.verify["type"] == "failure" and
                    self.verify["switch"].active ):
                self.retry()
            else:
                self.confirm_eject()



class Search(object):

    running = False
    index = 0
    timer = None

    def __call__(self):
        if self.running:
            log.warn("search already running")
            return
        log.debug("searching")
        p.notify("game", "Ball Search")
        self.running = True
        self.next()

    def next(self):
        search_sequence[self.index].pulse()
        self.index += 1
        if self.index == len(search_sequence):
            self.index = 0
            self.running = False
        else:
            self.timer = p.timers.wait(search_interval, self.next)


class Mode(Handler):

    history = collections.deque(maxlen=5)

    def setup(self):
        p.events.on("playfield_enable", self.enable)
        p.events.on("playfield_disable", self.disable)
        self.on("switch_active", self.switch_active)

    def switch_active(self, switch=None):
        if not "user" in switch.tags:
            self.history.appendleft(switch)
        for shot_name, rules in shots.items():
            self.evaluate_shot(shot_name, rules)

    def evaluate_shot(self, shot_name, rules):
        for rule, switch in zip(rules, self.history):
            if "eq" in rule and rule["eq"].name != switch.name:
                return
            elif "neq" in rule and rule["neq"].name == switch.name:
                return
            elif "eq" not in rule and "neq" not in rule:
                raise ValueError("Invalid rule in {}: {}".format(shot_name,
                        rule))
        shot_log.debug("+ {}".format(shot_name))
        p.events.trigger(shot_name)

    def on_disable(self):
        self.history.clear()



def in_trough():
    amount = 0
    for capture in captures.values():
        balls = capture.balls()
        if capture.name == "trough":
            amount += balls
        if capture.staged:
            if balls > capture.staged:
                balls = capture.staged
            amount += balls
    return amount

def in_play():
    return total - in_trough()

def missing():
    return in_play() > 0

def dead():
    return in_trough() == total

def status():
    log.debug("in play {}, in trough {}".format(in_play(), in_trough()))

search = Search()





