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

from pygame.locals import *
from ... import p, util
from .effect import Effect

class Laser(Effect):

    def __init__(self, target, duration=0.1, wait=2.0):
        durations = [duration] * target.height
        durations += [wait]
        super(Laser, self).__init__("laser", target, durations, repeat=True,
                once=False)
        self.target = target

    def action(self, *args, **kwargs):
        print "hello"
        self.target.invalidate()

    def post_render(self, frame):
        width = frame.get_width()
        height = frame.get_height()
        print "lasering", self.index, height, self.target
        if self.index <= height:
            if self.index - 1 >= 0:
                frame.fill(0x8, (0, self.index - 1, width, 1), BLEND_SUB)
            frame.fill(0x0, (0, self.index, width, 1))
            if self.index + 1 < height:
                frame.fill(0x8, (0, self.index + 1, width, 1), BLEND_SUB)

p.effects["laser"] = Laser
