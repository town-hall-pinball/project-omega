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

    def setup(self):
        self.display = ui.Panel(name="virtual_pallette")

        height = dmd.height / 4.0
        width = dmd.width / 4.0

        x = 0
        y = 0
        for i in xrange(16):
            color = 0xf if i < 8 else 0
            label = ui.Text(str(i), fill=i, left=x, top=y, width=width,
                    height=height, font="a5", color=color, case="title",
                    y_align="top")
            label.offset_y -= 3
            self.display.add(label)
            y += height
            if i % 4 == 3:
                y = 0
                x += width
        self.on("switch_service_exit",  self.exit)

    def on_disable(self):
        p.modes["service"].resume()

    def exit(self):
        p.mixer.play("service_exit")
        self.disable()
