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

import p
from . import display

class DMD(object):

    def __init__(self, options=None):
        options = options or {}
        palette_name = options.get("palette", "white")
        if palette_name not in self.palettes:
            raise ValueError("No such palette: {}".format(palette_name))

        self.dot_width = options.get("width", 128)
        self.dot_height = options.get("height", 32)
        self.multiplier = options.get("multiplier", 4)
        self.background_color = options.get("background_color", [0, 0, 0])
        self.border_color = options.get("border_color", [80, 80, 80])
        self.border_width = options.get("border_width", 20)
        self.border_height = options.get("border_height", 20)
        self.padding = options.get("padding", 1)
        self.debug = options.get("debug", False)
        self.palette = self.palettes[palette_name]

        self.width = (
            (self.dot_width * self.multiplier) +
            (self.padding * self.dot_width) +
            self.padding +
            (self.border_width * 2)
        )
        self.height = (
            (self.dot_height * self.multiplier) +
            (self.padding + self.dot_height) +
            self.padding +
            (self.border_height * 2)
        )
        display.init(self.width, self.height)

        self.dots = []
        self.previous = pygame.Surface((p.dmd_width, p.dmd_height))
        self.invalidate()

    def invalidate(self):
        target = display.get()

        target.fill(self.border_color,
                pygame.Rect(0, 0, self.width, self.height))
        target.fill(self.background_color,
                pygame.Rect(self.border_width, self.border_height,
                        self.width - (self.border_width * 2),
                        self.height - (self.border_height * 2)))

        if self.debug:
            target.fill(0xffffff, pygame.Rect(0, 0, self.width, self.height))

        for x in xrange(p.dmd_width):
            self.dots += [[]]
            for y in xrange(p.dmd_height):
                px = (self.border_width + self.padding +
                        (self.padding + self.multiplier) * x)
                py = (self.border_height + self.padding +
                        (self.padding + self.multiplier) * y)
                rect = pygame.Rect(px, py, self.multiplier, self.multiplier)
                self.dots[x] += [rect]
        pygame.display.update()

    def update(self, frame):
        source = pygame.PixelArray(frame)
        previous = pygame.PixelArray(self.previous)
        target = display.get()
        updates = []
        for x in xrange(0, self.dot_width):
            for y in xrange(0, self.dot_height):
                if source[x, y] != previous[x, y]:
                    index = source[x, y] & 0xf
                    target.fill(self.palette[index], self.dots[x][y])
                    updates += [self.dots[x][y]]
        pygame.display.update(updates)
        self.previous = frame


    palettes = {
        "orange": [
            (0, 0, 0),
            (15, 8, 0),
            (33, 17, 0),
            (51, 25, 0),
            (66, 33, 0),
            (84, 42, 0),
            (102, 51, 0),
            (117, 58, 0),
            (135, 67, 0),
            (153, 76, 0),
            (168, 84, 0),
            (186, 93, 0),
            (204, 102, 0),
            (219, 109, 0),
            (237, 118, 0),
            (255, 127, 0),
        ],
        "red": [
            (0, 0, 0),
            (15, 0, 0),
            (33, 0, 0),
            (51, 0, 0),
            (66, 0, 0),
            (84, 0, 0),
            (102, 0, 0),
            (117, 0, 0),
            (135, 0, 0),
            (153, 0, 0),
            (168, 0, 0),
            (186, 0, 0),
            (204, 0, 0),
            (219, 0, 0),
            (237, 0, 0),
            (255, 0, 0),
        ],
        "green": [
            (0, 0, 0),
            (0, 15, 0),
            (0, 33, 0),
            (0, 51, 0),
            (0, 66, 0),
            (0, 84, 0),
            (0, 102, 0),
            (0, 117, 0),
            (0, 135, 0),
            (0, 153, 0),
            (0, 168, 0),
            (0, 186, 0),
            (0, 204, 0),
            (0, 219, 0),
            (0, 237, 0),
            (0, 255, 0),
        ],
        "white": [
            (0, 0, 0),
            (15, 15, 15),
            (33, 33, 33),
            (51, 51, 51),
            (66, 66, 66),
            (84, 84, 84),
            (102, 102, 102),
            (117, 117, 117),
            (135, 135, 135),
            (153, 153, 153),
            (168, 168, 168),
            (186, 186, 186),
            (204, 204, 204),
            (219, 219, 219),
            (237, 237, 237),
            (255, 255, 255),
        ],
    }
