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
from pin import brand, ui
from . import system
from pin.ui.transitions import SlideIn, SlideOut
from pin.handler import Handler

class Mode(Handler):

    thp = ui.Image("thp_logo")
    presents = ui.Text("PRESENTS")
    title = ui.Text(brand.name, font="t5exb")
    game_over = ui.Text("Game Over")

    def setup(self):
        self.show = ui.Slides("attract.show", (
            (self.thp,           3.0),
            (self.presents,      3.0, SlideIn(direction="left")),
            (self.title,         3.0),
            (self.game_over,     6.0)),
            repeat=True)

    def enabled(self):
        system.mode.enable()
        self.show.start()
        p.mixer.play("introduction")

    def disabled(self):
        pass

mode = None

def init():
    global mode
    mode = Mode("attract.mode")




