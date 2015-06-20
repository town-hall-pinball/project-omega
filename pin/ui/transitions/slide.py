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
from . import Transition

__all__ = ["SlideIn", "SlideOut"]

class Slide(Transition):

    def __init__(self, name, direction="left", duration=1.0):
        super(Slide, self).__init__(name, duration)
        self.direction = direction
        self.start_x = 0
        self.start_y = 0
        self.direction_x = 0
        self.direction_y = 0
        self.setup()

    def calc(self):
        x = 0
        y = 0
        if self.direction_x != 0:
            x = self.start_x + (self.direction_x * p.dmd.width * self.progress)
        if self.direction_y != 0:
            y = self.start_y + (self.direction_y * p.dmd.height * self.progress)
        return (x, y)


class SlideIn(Slide):

    def __init__(self, direction="left", duration=1.0):
        super(SlideIn, self).__init__("slide_in", direction, duration)

    def setup(self):
        if self.direction == "left":
            self.start_x = p.dmd.width
            self.direction_x = -1
        elif self.direction == "right":
            self.start_x = -p.dmd.width
            self.direction_x = 1
        elif self.direction == "down":
            self.start_y = -p.dmd.height
            self.direction_y = 1
        elif self.direction == "up":
            self.start_y = p.dmd.height
            self.direction_y = -1
        else:
            raise ValueError("Invalid direction: {}".format(self.direction))

    def draw(self):
        x, y = self.calc()
        self.frame.blit(self.before, (0, 0))
        self.frame.blit(self.after, (x, y))

    def __str__(self):
        return "slide_in"


class SlideOut(Slide):

    def __init__(self, direction="left", duration=1.0):
        super(SlideOut, self).__init__("slide_out", direction, duration)

    def setup(self):
        if self.direction == "left":
            self.direction_x = -1
        elif self.direction == "right":
            self.direction_x = 1
        elif self.direction == "down":
            self.direction_y = 1
        elif self.direction == "up":
            self.direction_y = -1
        else:
            raise ValueError("Invalid direction: {}".format(self.direction))

    def draw(self):
        x, y = self.calc()
        self.frame.blit(self.after, (0, 0))
        self.frame.blit(self.before, (x, y))

    def __str__(self):
        return "slide_out"

