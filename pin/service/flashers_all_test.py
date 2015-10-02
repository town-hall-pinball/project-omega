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

from ..lib import p, dmd, ui, util
from ..lib.devices import devices
from ..lib.handler import Handler
from .matrix import Matrix

class Mode(Handler):

    timer = None

    def setup(self):
        self.display = ui.Panel(name="flashers_all_test")

        self.icon = ui.Image("service_flashers", left=0)
        self.title = ui.Text("All Flashers", font="t5b")
        self.light_label = ui.Text("Cycle", font="t5cp",
                padding=[1,5], fill=0x8)
        ui.valign((self.title, self.light_label))

        self.display.add([self.icon, self.title, self.light_label])
        self.on("switch_service_exit",  self.exit)

        compare = lambda x, y: cmp(x.label, y.label)
        self.flashers = util.Cycle(sorted(p.flashers.values(), cmp=compare))

    def on_enable(self):
        self.flashers.index = -1
        self.flash()

    def flash(self):
        self.cancel(self.timer)
        flasher = self.flashers.next()
        flasher.pulse(show=True)
        self.timer = self.wait(0.1, self.flash)

    def exit(self):
        self.disable()
        p.mixer.play("service_exit")

    def on_disable(self):
        self.cancel(self.timer)
        p.modes["service"].resume()
