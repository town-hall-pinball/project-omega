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
from pin.ui import effects
from pin.handler import Handler
from . import banner

class Mode(Handler):

    def setup(self):
        self.panel = ui.Notice(duration=4.0, callback=self.done)
        self.message = ui.Text("SETTINGS CLEARED", padding=2)
        self.panel.add(self.message)

    def enabled(self):
        if p.data.get("cleared", False):
            p.mixer.play("settings_cleared")
            effects.fill_blink(self.message, duration=0.25, repeat=2)
            self.panel.enqueue()
        else:
            self.disable()

    def disabled(self):
        banner.mode.enable()

    def done(self):
        self.disable()

mode = None

def init():
    global mode
    mode = Mode("post.mode")
