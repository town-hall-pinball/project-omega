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
from pin.handler import Handler
from . import attract

class Mode(Handler):

    def setup(self):
        self.panel = ui.Notice(
            "banner",
            duration=8,
            callback=self.done
        )
        self.title = ui.Text(
            brand.name,
            font="t5exb"
        )
        self.version = ui.Text(
            "Version {}".format(brand.version),
            font="t5cpb"
        )
        self.release = ui.Text(
            brand.release,
            font="t5cpb"
        )
        self.panel.add((self.title, self.version, self.release))

        self.on("switch_flipper_left", self.bypass)
        self.on("switch_flipper_right", self.bypass)
        self.on("switch_start_button", self.bypass)

    def enabled(self):
        self.panel.enqueue()
        p.mixer.play("boot")

    def bypass(self):
        self.panel.done()

    def done(self):
        self.disable()
        p.mixer.stop()
        attract.mode.enable()

mode = None

def init():
    global mode
    mode = Mode("banner.mode")
