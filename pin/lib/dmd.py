# Copyright (c) 2014 - 2016 townhallpinball.org
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

import itertools
import logging
import pygame

width = 128
height = 32

log = logging.getLogger("pin.dmd")

class DMD(object):

    def __init__(self):
        self.renderer = None
        self.previous_renderer = None

        self.frame = pygame.Surface((width, height))
        self.previous_frame = pygame.Surface((width, height))

        self.frame_from = pygame.Surface((width, height))
        self.frame_to = pygame.Surface((width, height))

        self.transition = None
        self.override = None
        self.stack = []
        self.queue = []

    def add(self, renderer, transition=None):
        if renderer in self.stack:
            return
        self.add_renderer(self.stack, renderer, transition)

    def enqueue(self, renderer, transition=None):
        if renderer in self.queue:
            return
        self.add_renderer(self.queue, renderer, transition)

    def interrupt(self, renderer):
        self.override = renderer
        self.override.render_start()
        log.debug("interrupting with {}".format(renderer))

    def replace(self, previous, current, transition=None):
        trans = "using {}".format(transition) if transition else ""
        log.debug("{} replaces {} {}".format(current, previous, trans))
        if previous in self.stack:
            self.stack[self.stack.index(previous)] = current
        elif previous in self.queue:
            self.queue[self.queue.index(previous)] = current
        else:
            transition = None
            self.stack += [current]
        self.shift_renderer(transition)

    def clear(self):
        for renderer in self.queue:
            renderer.on_render_stop()
        self.queue[:] = []
        if self.override:
            self.override.on_render_stop()
            self.override = None
        self.shift_renderer()

    def reset(self):
        if self.renderer:
            self.renderer.on_render_stop()
        if self.previous_renderer:
            self.previous_renderer.on_render_stop()
        self.renderer = None
        self.previous_renderer = None
        self.stack[:] = []
        self.clear()
        self.transition = None

    def add_renderer(self, collection, renderer, transition=None):
        trans = "using {}".format(transition) if transition else ""
        log.debug("{} added {}".format(renderer, trans))
        collection += [renderer]
        self.shift_renderer(transition)

    def remove(self, renderer):
        if renderer == self.override:
            self.override.render_stop()
            self.override = None
            return
        if renderer in self.stack:
            self.stack.remove(renderer)
        if renderer in self.queue:
            self.queue.remove(renderer)
        self.shift_renderer()

    def shift_renderer(self, transition=None):
        if len(self.queue) > 0:
            renderer = self.queue[0]
        elif len(self.stack) > 0:
            renderer = self.stack[-1]
        else:
            renderer = None

        if self.previous_renderer in self.stack:
            self.previous_renderer.render_suspend()
        elif self.previous_renderer:
            self.previous_renderer.render_stop()

        if self.renderer:
            self.renderer.render_stop()
            self.previous_renderer = self.renderer

        if not renderer:
            self.renderer = None
        else:
            if transition:
                transition.reset()
            elif self.renderer in self.stack:
                self.renderer.render_suspend()
            elif self.renderer:
                self.renderer.render_stop()
            self.renderer = renderer
            self.transition = transition
            self.renderer.render_start()

    def render(self):
        self.frame, self.previous_frame = self.previous_frame, self.frame
        self.frame.fill(0)

        if self.override:
            self.override.render(self.frame)
            return self.frame

        if not self.renderer and (len(self.stack) > 0 or len(self.queue) > 0):
            raise ValueError("No Renderer")
        elif not self.renderer:
            return

        if self.transition and self.transition.done:
            self.transition = None
            if self.renderer != self.previous_renderer:
                self.previous_renderer.render_stop()
            self.previous_renderer = None

        if self.transition:
            self.frame_from.fill(0)
            self.frame_to.fill(0)
            self.renderer.render(self.frame_to)
            self.previous_renderer.render(self.frame_from)
            self.transition.render(self.frame, self.frame_from, self.frame_to)
        else:
            self.renderer.render(self.frame)

        return self.frame


dmd = DMD()

add = dmd.add
replace = dmd.replace
interrupt = dmd.interrupt
remove = dmd.remove
enqueue = dmd.enqueue
clear = dmd.clear
reset = dmd.reset
render = dmd.render

def create_frame(width=width, height=height, has_alpha=True):
    if has_alpha:
        return pygame.Surface((width, height), pygame.locals.SRCALPHA)
    else:
        return pygame.Surface((width, height))

def create_dots(frame):
    return pygame.PixelArray(frame)


