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

from .. import p, util
from .misc import valign
from .panel import Panel
from .text import Text

class Notice(Panel):

    def __init__(self, duration=None, callback=None,
            defaults=None, **style):
        defaults = defaults or {}
        style["duration"] = duration
        style["padding"] = style.get("padding", 2)
        super(Notice, self).__init__(defaults, **style)
        self.timer = None
        self.callback = callback

    def add(self, components):
        for component in util.to_list(components):
            component.update(case="title")
        super(Notice, self).add(components)
        valign(self.children)

    def on_render_start(self):
        if self.style["duration"]:
            self.timer = p.timers.wait(self.style["duration"], self.done)

    def on_render_stopped(self):
        p.timers.cancel(self.timer)

    def done(self):
        p.timers.cancel(self.timer)
        p.dmd.remove(self)
        if self.callback:
            self.callback()


def notify(messages, duration=2.0, callback=None):
    panel = Notice(duration=duration, callback=callback)
    for message in util.to_list(messages):
        panel.add(Text(message, font="bm6"))
    p.dmd.interrupt(panel)

def message(message, duration=None, callback=None):
    panel = Notice(duration=duration, callback=callback)
    panel.add(Text(message))
    return panel




