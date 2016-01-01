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

import pygame

from pin.lib import brand, dmd
from pin.lib.virtual import palettes

multiplier = 4
"""
Each dot in the virutal displayed is multiplied by this number of pixels.
"""

background_color = [0, 0, 0]
"""
Background color as a list of red, green, and blue values between 0 and 255.
"""

border_color = [80, 80, 80]
"""
Border color as a list of red, green, and blue values between 0 and 255.
"""

border_width = 20
"""
Width of the border in pixels.
"""

border_height = 20
"""
Height of the border in pixels.
"""

x_padding = 1
"""
Padding, in pixels, between each dot in the horizontal direction.
"""

y_padding = 1
"""
Padding, in pixels, between each dot in the vertical direction.
"""

palette = palettes.gamma(1/2.2, palettes.green)
"""
An array that maps DMD brightness values (0 - 15) to RGB values for
the virtual display.
"""

width = 0
height = 0
dots = []
previous = pygame.Surface((dmd.width, dmd.height))

def init():
    """
    Creates and displays the virtual dot-matrix display.
    """
    invalidate()

def invalidate():
    """
    Call this function to invalidate the display when any of the styling
    parameters have changed.
    """
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
    pygame.display.set_caption(brand.name)
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
    """
    Update the virtual dot-matrix display to show the contents of `frame`.
    """
    global previous
    source = pygame.PixelArray(frame)
    previous = pygame.PixelArray(previous)
    target = pygame.display.get_surface()
    updates = []
    for x in xrange(0, dmd.width):
        for y in xrange(0, dmd.height):
            if source[x, y] != previous[x, y]:
                index = (source[x, y] >> 4) & 0xf
                target.fill(palette[index], dots[x][y])
                updates += [dots[x][y]]
    pygame.display.update(updates)
    previous = frame



