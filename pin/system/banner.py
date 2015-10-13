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

from pin.lib import p, brand, ui
from pin.lib.handler import Handler
from . import attract

class Mode(Handler):

    def setup(self):
        self.display = ui.Notice(
            name="banner",
            callback=self.done
        )
        self.title = ui.Text(
            brand.name,
            font="t5exb"
        )
        self.version = ui.Text(
            brand.version,
            font="t5cpb"
        )
        self.release = ui.Text(
            brand.release,
            font="t5cpb"
        )
        self.display.add((self.title, self.version, self.release))

        self.on("switch_flipper_left", self.bypass)
        self.on("switch_flipper_right", self.bypass)
        self.on("switch_start_button", self.bypass)
        self.on("switch_service_enter", self.bypass)
        self.on("switch_service_exit", self.bypass)

    def on_enable(self):
        p.mixer.play("boot")
        self.wait(8, self.done)

    def bypass(self):
        self.done()

    def done(self):
        self.disable()
        p.mixer.stop()
        p.modes["core"].enable()
        p.modes["attract"].enable()
