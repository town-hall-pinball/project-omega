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

import math
import pygame.locals
from pin import dmd

__all__ = ["debug_frame", "halign", "valign"]

def valign(components, padding=4):
    height = 0
    for component in components:
        component.layout()
        height += component.height
    height += (len(components) - 1) * padding
    y = math.floor((dmd.height - height) / 2.0)
    for component in components:
        component.update(top=y)
        y += component.height + padding


def halign(components, padding=4):
    width = 0
    for component in components:
        component.layout()
        width += component.width
    width += (len(components) - 1) * padding
    x = math.floor((dmd.width - width) / 2.0)
    for component in components:
        component.update(left=x)
        x += component.width + padding

def debug_frame(frame):
    dots = dmd.create_dots(frame)
    width, height = frame.get_size()
    lines = []
    for y in xrange(height):
        line = []
        for x in xrange(width):
            v = dots[x, y]
            c = frame.unmap_rgb(v)
            print c



