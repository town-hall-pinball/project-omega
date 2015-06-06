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

from collections import OrderedDict
import itertools
import logging
import pygame

width = 128
height = 32

log = logging.getLogger("pin.dmd")

class Renderer(object):

    def __init__(self, renderer, name, delegate=None):
        self.renderer = renderer
        self.name = name
        self.delegate = delegate

    def __call__(self, frame):
        self.renderer.render(frame)

    def start(self):
        if self.delegate:
            self.delegate.render_started()
        else:
            self.renderer.render_started()

    def restart(self):
        if self.delegate:
            self.delegate.render_restarted()
        else:
            self.renderer.render_restarted()

    def stop(self):
        if self.delegate:
            self.delegate.render_stopped()
        else:
            self.renderer.render_stopped()


class NullRenderer(Renderer):

    def __init__(self):
        super(NullRenderer, self).__init__(None, "null")

    def __call__(self, frame):
        pass

    def start(self):
        pass

    def restart(self):
        pass

    def stop(self):
        pass


class DMD(object):

    def __init__(self):
        self.renderer = None
        self.previous_renderer = None

        self.frame = pygame.Surface((width, height))
        self.previous_frame = pygame.Surface((width, height))

        self.frame_from = pygame.Surface((width, height))
        self.frame_to = pygame.Surface((width, height))

        self.transition = None
        self.stacked = OrderedDict()
        self.queued = OrderedDict()

        null = NullRenderer()
        self.stacked[null.name] = null

    def stack(self, name, renderer, transition=None, delegate=None):
        self.add(self.stacked, Renderer(renderer, name, delegate), transition)

    def enqueue(self, name, renderer, transition=None, delegate=None):
        self.add(self.queued, Renderer(renderer, name, delegate), transition)

    def add(self, collection, renderer, transition=None):
        trans = "using {}".format(transition.name) if transition else ""
        replaced = renderer.name in collection
        action = "replaced" if replaced else "added"
        log.debug("{} {} {}".format(renderer.name, action, trans))
        collection[renderer.name] = renderer
        self.shift_renderer(transition)
        if replaced:
            renderer.restart()

    def remove(self, name):
        if name in self.stacked:
            self.stacked.pop(name)
        if name in self.queued:
            self.queued.pop(name)
        self.shift_renderer()

    def shift_renderer(self, transition=None):
        if len(self.queued) > 0:
            renderer = self.queued.values()[0]
        else:
            renderer = self.stacked.values()[-1]
        notify = not(self.renderer and self.renderer.name == renderer.name)
        if self.previous_renderer:
            if notify:
                self.previous_renderer.stop()
            self.previous_renderer = None
        if transition:
            self.previous_renderer = self.renderer
            transition.reset()
        elif self.renderer:
            if notify:
                self.renderer.stop()
        self.renderer = renderer
        self.transition = transition
        if notify:
            self.renderer.start()

    def render(self):
        self.frame, self.previous_frame = self.previous_frame, self.frame
        self.frame.fill(0)

        if self.transition and self.transition.done:
            self.transition = None
            if self.renderer.name != self.previous_renderer.name:
                self.previous_renderer.stop()
            self.previous_renderer = None

        if self.transition:
            self.frame_from.fill(0)
            self.frame_to.fill(0)
            self.renderer(self.frame_to)
            self.previous_renderer(self.frame_from)
            self.transition.render(self.frame, self.frame_from, self.frame_to)
        else:
            self.renderer(self.frame)

        return self.frame


dmd = DMD()

stack = dmd.stack
remove = dmd.remove
enqueue = dmd.enqueue
render = dmd.render

def create_frame(width=width, height=height):
    return pygame.Surface((width, height))

def create_dots(frame):
    return pygame.PixelArray(frame)


