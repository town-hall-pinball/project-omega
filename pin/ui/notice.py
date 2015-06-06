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

import p
from .misc import valign
from .panel import Panel

class Notice(Panel):

    def __init__(self, name, duration=2.0, defaults=None, **style):
        defaults = defaults or {}
        style["duration"] = duration
        style["padding"] = style.get("padding", 2)
        super(Notice, self).__init__(defaults, **style)
        self.name = name
        self.timer = None

    def add(self, *components):
        super(Notice, self).add(*components)
        valign(self.children)

    def enqueue(self):
        p.dmd.enqueue(self.name, self)

    def render_started(self):
        self.timer = p.timers.set(self.style["duration"], self.done)

    def render_stopped(self):
        p.timers.clear(self.timer)

    def render_restarted(self):
        p.timers.clear(self.timer)
        self.timer = p.timers.set(self.style["duration"], self.done)

    def done(self):
        p.dmd.remove(self.name)


