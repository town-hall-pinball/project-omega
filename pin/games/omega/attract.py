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
from pin.ui.transitions import SlideIn, SlideOut
from pin.handler import Handler

class Mode(Handler):

    thp = ui.Image("thp_logo")
    texta = ui.Panel()
    text1 = ui.Text("ABCDEFGHIJKLM", top=5)
    text2 = ui.Text("NOPQRSTUVWXYZ", bottom=5)
    textb = ui.Panel()
    text3 = ui.Text("0123456789", top=5)
    text4 = ui.Text("1,2.3@#)", bottom=5)
    presents = ui.Text("Presents")
    title = ui.Text("Project Omega")
    game_over = ui.Text("Game Over")

    def setup(self):
        self.texta.add(self.text1, self.text2)
        self.textb.add(self.text3, self.text4)
        self.show = ui.Slides("attract.show", (
            #(self.thp,           3.0),
            (self.texta,          3.0),
            (self.textb,          3.0),
            (self.presents,      3.0, SlideIn(direction="left")),
            (self.title,         3.0),
            (self.game_over,     3.0)),
            repeat=True)
        self.handlers += [self.show]

    def enabled(self):
        self.show.start()

mode = None

def init():
    global mode
    mode = Mode("attract.mode")




