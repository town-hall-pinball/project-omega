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
from pin import dmd, ui, util
from pin.devices import devices
from pin.handler import Handler
from .matrix import Matrix

class Mode(Handler):

    def setup(self):
        self.display = ui.Panel(name="switch_single_test")
        self.matrix = Matrix(handler=self)
        self.info_width = dmd.width - self.matrix.width

        self.status = ui.Text("OPEN",
                left=self.matrix.width, width=self.info_width,
                font="t5cpb", x_align="center")
        self.name = ui.Text("Switch Name", left=self.matrix.width,
                width=self.info_width, font="t5cp", x_align="center",
                case="full")
        self.opto = ui.Text("Opto", left=self.matrix.width,
                width=self.info_width, font="t5cp", x_align="center")
        ui.valign((self.status, self.name, self.opto))

        self.display.add([self.matrix, self.status, self.name, self.opto])

        compare = lambda x, y: cmp(x.label, y.label)
        ordered_switches = sorted(p.switches.values(), cmp=compare)
        self.iter = util.Cycle(ordered_switches)

        self.on("switch_service_exit",  self.exit)
        self.on("switch_service_up", self.next)
        self.on("switch_service_down", self.previous)
        self.on("switch", self.update_switches)
        self.update_selection()

    def on_enable(self):
        self.update_switches()

    def update_switches(self, sw=None, state=None):
        self.matrix.redraw()
        if sw and sw == self.iter.get():
            self.update_selection_status()
        if sw and sw.active:
            p.mixer.play("service_switch_edge")

    def update_selection(self):
        switch = self.iter.get()
        self.matrix.select(switch)
        self.name.show(switch.label)
        if switch.opto:
            self.opto.show("Opto")
        else:
            self.opto.hide()
        self.update_selection_status()

    def update_selection_status(self):
        switch = self.iter.get()
        if switch.is_opened():
            self.status.show("Open")
        else:
            self.status.show("Closed")

    def next(self):
        self.iter.next()
        self.update_selection()

    def previous(self):
        self.iter.previous()
        self.update_selection()

    def exit(self):
        self.disable()
        p.mixer.play("service_exit")

    def on_disable(self):
        p.modes["service"].resume()
