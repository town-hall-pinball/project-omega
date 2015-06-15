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
from pin import util
from pin.handler import Handler


class Slides(util.Show):

    def __init__(self, name, slides, **kwargs):
        timings = [x[1] for x in slides]
        super(Slides, self).__init__(name, timings, **kwargs)
        self.slides = []
        self.transitions = []
        self.previous = None
        for i, item in enumerate(slides):
            self.slides += [item[0]]
            self.transitions += [None if len(item) != 3 else item[2]]

    def setup(self):
        self.on("switch_flipper_left", self.next)
        self.on("switch_flipper_right", self.next)

    def action(self, use_callback=False):
        if self.previous:
            self.previous.render_stopped()
        current = self.slides[self.index]
        p.dmd.stack(self.name, current, self.transitions[self.index],
                delegate=self)
        current.render_started()
        self.previous = current
        if use_callback:
            self.slides[self.index].start(self.next)

    def render_stopped(self):
        self.disable()
        self.stop()

    def render_started(self):
        self.enable()
        self.start()





