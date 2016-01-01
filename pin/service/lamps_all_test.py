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

from ..lib import p, dmd, ui, util
from ..lib.devices import devices
from ..lib.handler import Handler
from .matrix import Matrix

toggle_time = 1

class Mode(Handler):

    lamps_on = False
    timer = None

    def setup(self):
        self.display = ui.Panel(name="lamps_all_test")

        self.icon = ui.Image("service_lamps", left=0)
        self.title = ui.Text("All Lamps", font="t5b")
        self.light_label = ui.Text("Light", font="t5cp",
                padding=[1,5], fill=0x2, enabled=False)
        ui.valign((self.title, self.light_label))

        self.display.add([self.icon, self.title, self.light_label])
        self.on("switch_service_exit",  self.exit)

    def on_enable(self):
        self.lamps_on = False
        self.toggle()

    def toggle(self):
        self.cancel(self.timer)
        self.lamps_on = not self.lamps_on
        if self.lamps_on:
            self.light_label.show("Light")
        else:
            self.light_label.hide()
        self.light()
        self.timer = self.wait(toggle_time, self.toggle)

    def light(self):
        map(lambda l: l.enable(self.lamps_on, show=True), p.lamps.values())

    def exit(self):
        self.disable()
        p.mixer.play("service_exit")

    def on_disable(self):
        self.lamps_on = False
        self.light()
        p.modes["service"].resume()


