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

import math
import pin
from pin import util

class Component(object):

    frame = None
    dirty = False
    width = None
    height = None
    x = None
    y = None
    parent = None
    children = None
    enabled = True

    def __init__(self, defaults=None, **style):
        self.style = {}
        self.children = []
        self.defaults = {
            "top": None,
            "right": None,
            "bottom": None,
            "left": None,
            "width": None,
            "height": None,
            "fill": 0,
            "padding_top": 0,
            "padding_right": 0,
            "padding_bottom": 0,
            "padding_left": 0,
            "x_align": "center",
            "y_align": "center",
        }
        if defaults:
            self.defaults.update(defaults)
        self.set(**style)

    def set(self, **style):
        self.style.clear()
        self.update(**self.defaults)
        self.update(**style)
        self.invalidate()

    def update(self, **style):
        self.style.update(style)
        if "padding" in style:
            self.expand4("padding", util.to_list(style["padding"]))
        self.invalidate()

    def invalidate(self):
        self.dirty = True
        if self.parent:
            self.parent.invalidate()

    def revalidate(self):
        for child in self.children:
            if child.dirty:
                child.revalidate()
        self.layout()
        self.draw()
        self.dirty = False

    def layout(self):
        style = self.style
        self.width = None
        self.height = None

        if style["width"] != None:
            self.width = style["width"]
        if style["height"] != None:
            self.height = style["height"]

        if self.width == None:
            if style["left"] != None and style["right"] != None:
                self.width = pin.dmd.width - style["left"] - style["right"]
        if self.height == None:
            if style["top"] != None and style["bottom"] != None:
                self.height = pin.dmd.height - style["top"] - style["bottom"]

        if self.width == None or self.height == None:
            self.auto_size()

        self.x = None
        self.y = None

        # See if can be anchored to top left
        if style["left"] != None:
            self.x = style["left"]
        if style["top"] != None:
            self.y = style["top"]

        # See if can be anchored to bottom right
        if self.x == None and style["right"] != None:
            self.x = pin.dmd.width - self.width - style["right"]
        if self.y == None and style["bottom"] != None:
            self.y = pin.dmd.height - self.height - style["bottom"]

        if self.x == None:
            self.x = math.floor((pin.dmd.width - self.width) / 2.0)
        if self.y == None:
            self.y = math.floor((pin.dmd.height - self.height) / 2.0)

    def auto_size(self):
        if self.width == None:
            self.width = pin.dmd.width
        if self.height == None:
            self.height = pin.dmd.height

    def render(self, target):
        if not self.enabled:
            return
        if self.dirty:
            self.revalidate()
        target.blit(self.frame, (self.x, self.y))

    def render_started(self):
        pass

    def render_stopped(self):
        pass

    def render_restarted(self):
        pass

    def draw(self):
        if ( not self.frame or self.width > self.frame.get_width() or
                self.height > self.frame.get_height() ):
            self.frame = pin.dmd.create_frame(self.width, self.height)

        fill = self.style["fill"]
        self.frame.fill(fill, (0, 0, self.width, self.height))

    def expand4(self, key, value):
        if len(value) == 1:
            value = [value[0], value[0], value[0], value[0]]
        elif len(value) == 2:
            value = [value[0], value[1], value[0], value[1]]
        elif len(value) == 3:
            value = [value[0], value[1], value[2], value[1]]
        self.style[key + "_top"] = value[0]
        self.style[key + "_right"] = value[1]
        self.style[key + "_bottom"] = value[2]
        self.style[key + "_left"] = value[3]




