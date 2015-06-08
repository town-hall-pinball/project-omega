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

from pin import util

class Blink(util.Show):

    def __init__(self, target, duration=0.5, repeat=False):
        super(Blink, self).__init__("blink",
                [duration, duration], repeat)
        self.target = target

    def action(self):
        if self.index % 2 == 1:
            self.target.update(color=0xf)
        else:
            self.target.update(color=0x0)

def blink(target, duration=0.5, repeat=False):
    Blink(target, duration, repeat).start()


class FillBlink(util.DMDShow):

    def __init__(self, target, duration=0.5, repeat=False):
        super(FillBlink, self).__init__("fill_blink",
                [duration, duration], repeat)
        self.target = target

    def action(self):
        if self.index % 2 == 1:
            self.target.update(color=0xf, fill=0x0)
        else:
            self.target.update(color=0x0, fill=0x0f)

def fill_blink(target, duration=0.5, repeat=False):
    FillBlink(target, duration, repeat).start()



