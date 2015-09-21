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

from pin import dmd
from pin.devices import devices
from pin.ui import Canvas

class Matrix(Canvas):

    box_when = "closed"
    devices = None
    selected = None
    pulse_color = 0x8
    pulse_timer = None
    handler = None

    def __init__(self, handler=None, box_when=None, devices="switches"):
        super(Matrix, self).__init__(left=0, top=0, width=40)
        if box_when:
            self.box_when = box_when
        self.devices = devices
        self.handler = handler
        self.layout()

    def redraw(self):
        self.clear()
        if self.devices == "switches":
            self.dot_column(2, "SD")
            self.vline(5, 2, dmd.height - 4, color=0x8)
        col = 1
        for x in xrange(8, 8 + (8 * 3), 3):
            prefix = "S" if self.devices == "switches" else "L"
            self.dot_column(x, prefix + str(col))
            col += 1
        x += 3
        if self.devices == "switches":
            self.vline(x, 2, dmd.height - 4, color=0x8)
            x += 3
            self.dot_column(x, "SF")
        self.invalidate()

    def select(self, switch):
        self.handler.cancel(self.pulse_timer)
        self.selected = switch
        if self.handler and self.selected:
            self.pulse_selection()
        elif self.handler and not self.selected:
            self.redraw()

    def pulse_selection(self):
        self.pulse_color += 0x2
        if self.pulse_color > 0xf:
            self.pulse_color = 0x8
        self.redraw()
        self.pulse_timer = self.handler.wait(0.1, self.pulse_selection)

    def cell_rendering(self, device):
        if not device:
            return "empty"
        if device == self.selected:
            return "selected"
        if self.devices == "switches":
            if self.box_when == "closed" and device.is_closed():
                return "box"
            if self.box_when == "active" and device.active:
                return "box"
        else:
            if device.is_active():
                return "box"
        return "dot"

    def dot_column(self, x, prefix):
        y = 5
        row = 1
        for y in xrange(5, 5 + (8 * 3), 3):
            ident = prefix + str(row)
            device = devices.get(ident)
            rendering = self.cell_rendering(device)
            if rendering == "box":
                self.box(x - 1, y - 1, 3, 3)
            elif rendering == "dot":
                self.dot(x, y)
            elif rendering == "selected":
                self.dot(x, y, self.pulse_color)
                self.dot(x-1, y-1, self.pulse_color)
                self.dot(x-1, y+1, self.pulse_color)
                self.dot(x+1, y-1, self.pulse_color)
                self.dot(x+1, y+1, self.pulse_color)
            row += 1

