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
from .. import attract

class Coin(Handler):

    def setup(self):
        self.credits = ui.Notice("credit_display", duration=3)
        self.amount = ui.Text("CREDITS 0")
        self.message = ui.Text("FREE PLAY")
        self.credits.add((self.amount, self.message))

        self.on("switch_start_button", self.start_button)
        self.on("switch_coin_left", self.coin_left)
        self.update()

    def start_button(self):
        self.update()
        if attract.mode.active:
            self.credits.enqueue()

    def coin_left(self):
        self.paid_credit(0.25)

    def paid_credit(self, value):
        pricing = p.data["pricing"]
        add = value / pricing
        p.data["earnings"] += value
        p.data["paid_credits"] += add
        self.add_credit(add)

    def add_credit(self, add=1):
        if p.data["credits"] >= p.data["max_credits"]:
            return
        p.data["credits"] += add
        p.mixer.play("coin_drop")
        self.update()
        if attract.mode.active and not p.data["free_play"]:
            self.credits.enqueue()

    def update(self):
        free_play = p.data["free_play"]
        credits = p.data["credits"]

        if free_play:
            self.amount.show("FREE PLAY")
        else:
            self.amount.show("CREDITS {}".format(util.fraction(credits)))

        if free_play or credits >= 1:
            self.message.show("PRESS START")
            self.message.do(ui.effects.Pulse(self.message))
        else:
            self.message.show("INSERT COINS")
            self.message.do(ui.effects.Blink(self.message, duration=0.2,
                    repeat=3))



handler = None

def init():
    global handler
    handler = Coin("system.coin.handler")
