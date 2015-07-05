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
from pin import ui, util
from pin.handler import Handler

class CreditsDisplay(object):

    def __init__(self):
        self.display = ui.Notice(name="credits")
        self.amount = ui.Text("CREDITS 0.00")
        self.message = ui.Text("FREE PLAY")
        self.display.add((self.amount, self.message))
        self.update()

        p.events.on("data_free_play", self.update)
        p.events.on("data_credits", self.update)

    def update(self):
        free_play = p.data["free_play"]
        credits = p.data["credits"]

        if free_play:
            self.amount.show("FREE PLAY")
        else:
            self.amount.show("CREDITS {:0.2f}".format(credits))

        if free_play or credits >= 1:
            self.message.show("PRESS START")
            self.message.effect("pulse")
        else:
            self.message.show("INSERT COINS")
            self.message.effect("blink", duration=0.2, repeat=3)

class Mode(Handler):

    def setup(self):
        self.timer = None
        self.credits = p.displays["credits"]

        self.on("switch_start_button",  self.start_button)
        self.on("switch_coin_left",     self.coin_left)
        self.on("switch_coin_center",   self.coin_center)
        self.on("switch_coin_right",    self.coin_right)
        self.on("switch_coin_fourth",   self.coin_fourth)
        self.on("switch_service_exit",  self.service_credit)

    def start_button(self):
        if p.modes["attract"].enabled:
            self.show_credits()

    def show_credits(self):
        p.modes["attract"].suspend()
        p.dmd.enqueue(self.credits.display)
        self.cancel(self.timer)
        self.timer = self.wait(3.0, self.done)

    def done(self):
        p.dmd.remove(self.credits.display)
        p.modes["attract"].resume()
        self.cancel(self.timer)

    def coin_left(self):
        self.paid_credit(p.data["coin_left"])

    def coin_center(self):
        self.paid_credit(p.data["coin_center"])

    def coin_right(self):
        self.paid_credit(p.data["coin_right"])

    def coin_fourth(self):
        self.paid_credit(p.data["coin_fourth"])

    def paid_credit(self, value):
        pricing = p.data["pricing"]
        add = value / pricing
        p.data["earnings"] += value
        p.data["paid_credits"] += add
        self.add_credit(add)

    def service_credit(self):
        if not p.modes["service"].enabled:
            p.data["service_credits"] += 1
            self.add_credit(1)

    def add_credit(self, add=1):
        if p.data["credits"] >= p.data["max_credits"]:
            return
        p.data["credits"] += add
        p.mixer.play("coin_drop")
        if p.modes["attract"].enabled and not p.data["free_play"]:
            self.show_credits()
        p.data.save()
        p.events.post("credits")


def init():
    p.displays["credits"] = CreditsDisplay()
