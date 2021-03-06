# Copyright (c) 2014 - 2016 townhallpinball.org
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

import logging

from pin import machine
from pin.lib import p, ui
from pin.lib.ui import effects
from pin.lib.handler import Handler
from . import banner, display

log = logging.getLogger("pin")

class Mode(Handler):

    def setup(self):
        self.timer = None
        self.panel = None
        machine.user_bypass(self, self.done)

    def on_enable(self):
        if p.data.get("cleared", False):
            p.mixer.play("settings_cleared")
            self.panel = display.Info()
            self.show(self.panel)
            self.panel.description.update(padding_top=1)
            self.panel.description.show("Settings Cleared")
            self.panel.description.effect("fill_blink", duration=0.25, repeat=2)
            self.wait(5.0, self.done)
        elif p.data.get("simulator_enabled", False):
            p.mixer.play("warning")
            self.panel = display.Warning()
            self.show(self.panel)
            self.panel.description.show("Simulator On")
            self.panel.title.effect("blink", on=0.4, off=0.1, repeat=4)
            self.wait(5.0, self.done)
        else:
            self.disable()

    def on_disable(self):
        p.modes["banner"].enable()

    def done(self):
        self.cancel(self.timer)
        self.disable()

