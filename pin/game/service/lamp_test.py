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
from pin.devices import devices
from pin.handler import Handler
from pin import dmd, ui, util

class Mode(Handler):

    matrix_width = 40

    def setup(self):
        self.info_width = dmd.width - self.matrix_width
        self.display = ui.Panel(name="switch_test")
        self.canvas = ui.Canvas(left=0, top=0, width=self.matrix_width)

        self.title = ui.Text("Switch Edges", top=5, left=self.matrix_width,
                width=self.info_width, font="t5cpb", x_align="center")
        self.name = ui.Text(" ", left=self.matrix_width, bottom=5,
                width=self.info_width, font="t5cp", x_align="center",
                case="full")

        self.display.add([self.canvas, self.title, self.name])
        self.on("switch_service_exit",  self.exit)
        self.on("switch", self.update_switches)
