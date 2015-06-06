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
from pin import ui
from pin.handler import Handler

class Mode(Handler):

    def setup(self):
        self.credits = ui.Notice("credit_display")
        self.amount = ui.Text("CREDITS 0", top=0)
        self.message = ui.Text("INSERT COINS", bottom=0)
        self.credits.add(self.amount, self.message)

        self.more = ui.Notice("more")
        self.more2 = ui.Text("MORE STUFF")
        self.more.add(self.more2)

        self.on("switch_start_button", self.start_button)
        self.on("switch_coin_left", self.other)

    def start_button(self):
        self.credits.enqueue()

    def other(self):
        self.more.enqueue()

mode = None

def init():
    global mode
    mode = Mode("system.coin.mode")
