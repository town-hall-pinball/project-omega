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

from .. import dmd, util
from .component import Component

class Canvas(Component):

    def __init__(self, **style):
        super(Canvas, self).__init__(defaults={
            "color": 0xf,
            "width": dmd.width,
            "height": dmd.height,
        }, **style)
        self.canvas = dmd.create_frame(has_alpha=False)

    def clear(self):
        self.canvas.fill(0)

    def fill(self, left=0, top=0, width=dmd.width, height=dmd.height,
            color=None):
        color = (color or self.style["color"]) << 4
        self.canvas.fill(color, (left, top, width, height))

    def dot(self, x, y, color=None):
        color = (color or self.style["color"]) << 4
        self.canvas.set_at((x, y), color)

    def vline(self, x, top, length, color=None):
        color = (color or self.style["color"]) << 4
        self.canvas.fill(color, (x, top, 1, length))

    def hline(self, left, y, length, color=None):
        color = (color or self.style["color"]) << 4
        self.canvas.fill(color, (left, y, length, 1))

    def box(self, left, top, width, height, color=None):
        self.hline(left, top, width, color)
        self.hline(left, top + height - 1, width, color)
        self.vline(left, top, height, color)
        self.vline(left + width - 1, top, height, color)

    def draw(self):
        super(Canvas, self).draw()
        if self.width == 0 or self.height == 0:
            return
        self.frame.blit(self.canvas, (self.style["padding_left"],
                self.style["padding_top"]))

    def __str__(self):
        name = self.style.get("name", None)
        return "canvas({})".format(name) if name else "canvas"
