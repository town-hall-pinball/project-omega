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

    row = 1
    col = 0
    update_count = 0
    timer = None

    def setup(self):
        self.display = ui.Panel(name="switch_levels_test")
        self.matrix = Matrix(handler=self, box_when="active")
        self.info_width = dmd.width - self.matrix.width

        self.title = ui.Text("Switch Levels",
                left=self.matrix.width, width=self.info_width,
                font="t5cpb", x_align="center")
        self.name = ui.Text(" ", left=self.matrix.width,
                width=self.info_width, font="t5cp", x_align="center",
                case="full")
        ui.valign((self.title, self.name))

        self.display.add([self.matrix, self.title, self.name])
        self.on("switch_service_exit",  self.exit)
        self.on("switch_service_up", self.next)
        self.on("switch_service_down", self.previous)
        self.on("switch", self.update_switches)

    def on_enable(self):
        self.update_count = 0
        self.update_switches()
        self.advance_switch()
        self.update_active()

    def update_switches(self, sw=None, state=None):
        self.matrix.redraw()
        if sw and sw.active:
            p.mixer.play("service_switch_edge")
        if sw and not sw.active and sw == self.matrix.selected:
            self.advance_switch()

    def update_active(self):
        self.update_count += 1
        if self.update_count % 20 == 0:
            self.advance_switch()
            self.matrix.redraw()
        self.timer = self.wait(0.1, self.update_active)

    def advance_switch(self, direction=1):
        self.find_next_switch(direction)
        if not self.matrix.selected:
            self.name.show("None active")
        else:
            self.name.show(self.matrix.selected.label)

    def get_ident(self):
        r = self.row
        c = self.col
        if r == 0:
            r = "D"
        if r == 9:
            r = "F"
        return "S" + str(c) + str(r)

    def find_next_switch(self, direction=1):
        count = 0
        while True:
            count += 1
            self.row += direction
            if self.row >= 8:
                self.row = 0
                self.col += 1
                if self.col >= 10:
                    self.col = 0
            if self.row < 0:
                self.row = 7
                self.col -= 1
                if self.col < 0:
                    self.col = 9
            ident = self.get_ident()
            switch = devices.get(ident)
            if switch and switch.active:
                self.matrix.select(switch)
                return
            if count > 8 * 10:
                self.matrix.select(None)
                self.update_count = 0
                return

    def next(self):
        self.cancel(self.timer)
        self.update_count = 0
        self.advance_switch()
        self.update_active()

    def previous(self):
        self.cancel(self.timer)
        self.update_count = 0
        self.advance_switch(-1)
        self.update_active()

    def exit(self):
        self.disable()
        p.mixer.play("service_exit")

    def on_disable(self):
        p.modes["service"].resume()


