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

import pygame

from pin import dmd
from pin.virtual import palettes

multiplier = 4
background_color = [0, 0, 0]
border_color = [80, 80, 80]
border_width = 20
border_height = 20
x_padding = 1
y_padding = 1
palette = palettes.orange

width = 0
height = 0
dots = []
previous = pygame.Surface((dmd.width, dmd.height))

def init():
    invalidate()

def invalidate():
    global width, height, dots
    width = (
        (dmd.width * multiplier) +
        (x_padding * dmd.width) +
        x_padding +
        (border_width * 2)
    )
    height = (
        (dmd.height * multiplier) +
        (y_padding + dmd.height) +
        y_padding +
        (border_height * 2)
    )

    pygame.display.set_mode([width, height])
    target = pygame.display.get_surface()

    target.fill(border_color, pygame.Rect(0, 0, width, height))
    target.fill(background_color,
            pygame.Rect(border_width, border_height,
                    width - (border_width * 2),
                    height - (border_height * 2)))

    dots[:] = []
    for x in xrange(dmd.width):
        dots += [[]]
        for y in xrange(dmd.height):
            px = (border_width + x_padding + (x_padding + multiplier) * x)
            py = (border_height + y_padding + (y_padding + multiplier) * y)
            rect = pygame.Rect(px, py, multiplier, multiplier)
            dots[x] += [rect]
    pygame.display.update()

def update(frame):
    global previous
    source = pygame.PixelArray(frame)
    previous = pygame.PixelArray(previous)
    target = pygame.display.get_surface()
    updates = []
    for x in xrange(0, dmd.width):
        for y in xrange(0, dmd.height):
            if source[x, y] != previous[x, y]:
                index = source[x, y] & 0xf
                target.fill(palette[index], dots[x][y])
                updates += [dots[x][y]]
    pygame.display.update(updates)
    previous = frame



