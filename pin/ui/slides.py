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
import pin
from pin import util

class Slides(util.Show):

    def __init__(self, name, slides, **kwargs):
        self.slides = []
        self.transitions = []
        timings = []
        for item in slides:
            self.slides += [item[0]]
            timings += [item[1]]
            self.transitions += [None if len(item) != 3 else item[2]]
        self.name = None
        super(Slides, self).__init__(name, timings, **kwargs)

    def started(self):
        self.name = pin.dmd.add(self.slides[0])

    def stopped(self):
        pin.dmd.remove(self.name)

    def action(self):
        pin.dmd.replace(self.slides[self.index], self.name)
        transition = self.transitions[self.index]
        if transition:
            transition.reset()
            pin.dmd.transition = transition




