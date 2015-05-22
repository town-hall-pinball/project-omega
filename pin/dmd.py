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

class DMD(object):

    def __init__(self):
        self.frame = pygame.Surface((p.dmd_width, p.dmd_height))
        self.standard = []
        self.interrupts = []
        self.overlays = []

    def add(self, renderer):
        self.standard += [renderer]

    def remove(self, renderer):
        self.standard.remove(renderer)
        self.interrupts.remove(renderer)
        self.overlays.remove(renderer)

    def interrupt(self, renderer):
        self.interrupts += [renderer]

    def create_frame(self):
        return pygame.Surface((p.dmd_width, p.dmd_height))

    def create_dots(self, frame):
        return pygame.PixelArray(frame)

    def render(self):
        rendered = self.frame
        if len(self.interrupts) > 0:
            rendered = self.interrupts[0].render()
        elif len(self.standard) > 0:
            rendered = self.standard[-1].render()
        return rendered




