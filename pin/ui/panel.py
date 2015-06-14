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

import pin
from pin import util
from .component import Component

class Panel(Component):

    def __init__(self, defaults=None, **style):
        defaults = defaults or {}
        defaults["width"] = defaults.get("width", pin.dmd.width)
        defaults["height"] = defaults.get("height", pin.dmd.height)
        super(Panel, self).__init__(defaults, **style)

    def add(self, components):
        components = util.to_list(components)
        for component in components:
            self.children += [component]
            component.parent = self
            self.invalidate()

    def clear(self):
        self.children = []
        self.invalidate()

    def draw(self):
        super(Panel, self).draw()
        for child in self.children:
            self.frame.blit(child.frame,
                    (child.x, child.y, child.width, child.height))

    def __str__(self):
        name = self.style.get("name", None)
        return "panel({})".format(name) if name else "panel"

