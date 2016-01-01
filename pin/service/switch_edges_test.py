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

from ..lib.handler import Handler
from ..lib import p, dmd, ui, util
from .matrix import Matrix

class Mode(Handler):

    def setup(self):
        self.display = ui.Panel(name="switch_edges_test")
        self.matrix = Matrix()
        self.info_width = dmd.width - self.matrix.width

        self.title = ui.Text("Switch Edges",
                left=self.matrix.width, width=self.info_width,
                font="t5cpb", x_align="center")
        self.name = ui.Text(" ", left=self.matrix.width,
                width=self.info_width, font="t5cp", x_align="center",
                case="full")
        ui.valign((self.title, self.name))

        self.display.add([self.matrix, self.title, self.name])
        self.on("switch_service_exit",  self.exit)
        self.on("switch", self.update_switches)

    def on_enable(self):
        self.update_switches()

    def update_switches(self, sw=None, state=None):
        if sw:
            self.name.show(sw.label, duration=3)
        self.matrix.redraw()
        if sw and sw.active:
            p.mixer.play("service_switch_edge")

    def exit(self):
        self.disable()
        p.mixer.play("service_exit")

    def on_disable(self):
        p.modes["service"].resume()





