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

import p
import pin
from pin import util

class Component(object):

    def __init__(self, defaults=None, **style):
        self.frame = None
        self.dirty = False
        self.width = None
        self.height = None
        self.x = None
        self.y = None
        self.parent = None
        self.children = None
        self.enabled = True
        self.rendering = False
        self.suspended = False
        self.has_alpha = True
        self.style = {}
        self.children = []
        self.active_effect = None
        self.name = None
        self.show_timer = None
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
            "composite": 0,
        }
        if defaults:
            self.defaults.update(defaults)
        self.set(**style)

    def set(self, **style):
        self.style.clear()
        self.update(**self.defaults)
        self.update(**style)

    def effect(self, name, **kwargs):
        if self.active_effect:
            self.active_effect.stop()
        self.active_effect = p.effects[name](self, **kwargs)
        if self.rendering:
            self.active_effect.start()

    def update(self, **style):
        self.style.update(style)
        if "padding" in style:
            self.expand4("padding", util.to_list(style["padding"]))
        if "enabled" in style:
            if style["enabled"]:
                self.show()
            else:
                self.hide()
        if "name" in style:
            self.name = style["name"]
        self.invalidate()

    def show(self, duration=None):
        self.enabled = True
        self.invalidate()
        if duration:
            p.timers.clear(self.show_timer)
            self.show_timer = p.timers.set(duration, self.hide)

    def hide(self):
        self.enabled = False
        self.invalidate()
        p.timers.clear(self.show_timer)

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
        target.blit(self.frame, (self.x, self.y),
                special_flags=self.style["composite"])
        self.on_render()
        for child in self.children:
            child.on_render()

    def on_render(self):
        pass

    def render_start(self):
        self.rendering = True
        self.invalidate()
        if self.active_effect:
            self.active_effect.restart()

        if self.suspended:
            self.suspended = False
            self.on_render_resume()
        else:
            self.on_render_start()

        for child in self.children:
            child.render_start()

    def on_render_start(self):
        pass

    def render_stop(self):
        self.rendering = False
        self.suspended = False
        if self.active_effect:
            self.active_effect.stop()
        for child in self.children:
            child.render_stop()

    def on_render_stop(self):
        pass

    def render_suspend(self):
        self.suspended = True
        if self.active_effect:
            self.active_effect.stop()
        for child in self.children:
            child.render_suspend()

    def on_render_suspend(self):
        pass

    def on_render_resume(self):
        pass

    def draw(self):
        if self.width < 0 or self.height < 0:
            self.frame = pin.dmd.create_frame(1, 1)
            return
        if ( not self.frame or self.width > self.frame.get_width() or
                self.height > self.frame.get_height() ):
            self.frame = pin.dmd.create_frame(self.width, self.height,
                    self.has_alpha)
        fill = self.style.get("fill", None)

        self.frame.fill((0, 0, 0, 0), (0, 0, self.frame.get_width(),
                self.frame.get_height()))
        if fill is not None:
            self.frame.fill((fill * 16, fill * 16, fill * 16, 0xff),
                    (0, 0, self.width, self.height))

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




