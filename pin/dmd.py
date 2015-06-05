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

log = logging.getLogger("pin.dmd")

width = 128
height = 32

current_frame = pygame.Surface((width, height))
previous_frame = pygame.Surface((width, height))
previous_renderer = None
frame_after = pygame.Surface((width, height))
frame_before = pygame.Surface((width, height))

stack = OrderedDict()
interrupts = OrderedDict()
overlays = OrderedDict()
counter = itertools.count()

transition = None

def add(renderer, name=None):
    if not name:
        name = counter.next()
    stack[name] = get_renderer(renderer)
    log.debug("{} added".format(name))
    return name

def remove(name):
    if name in stack:
        stack.remove(name)
    if name in interrupts:
        interrupts.remove(name)
    if name in overlays:
        overlays.remove(name)
    log.debug("{} removed".format(name))

def replace(renderer, name):
    if name in stack:
        stack[name] = get_renderer(renderer)
    if name in interrupts:
        interrupts[name] = get_renderer(renderer)
    if name in overlays:
        overlays[name] = get_renderer(renderer)

def interrupt(renderer, name=None):
    if not name:
        name = counter.next()
    interrupts[name] = renderer
    return name

def create_frame(width=width, height=height):
    return pygame.Surface((width, height))

def create_dots(frame):
    return pygame.PixelArray(frame)

def render():
    global current_frame, previous_frame, previous_renderer, transition
    current_frame, previous_frame = previous_frame, current_frame
    current_frame.fill(0)

    if len(interrupts) > 0:
        current_renderer = interrupts.values()[0]
    elif len(stack) > 0:
        current_renderer = stack.values()[-1]

    if transition and transition.done:
        transition = None
    if transition:
        frame_after.fill(0)
        frame_before.fill(0)
        current_renderer(frame_after)
        previous_renderer(frame_before)
        transition.render(current_frame, frame_before, frame_after)
    else:
        current_renderer(current_frame)
        previous_renderer = current_renderer

    return current_frame

def get_renderer(r):
    return r.render if hasattr(r, "render") else r

