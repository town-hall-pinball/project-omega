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

import pygame

width = 128
height = 32

frame = pygame.Surface((width, height))
previous = pygame.Surface((width, height))

standard = []
interrupts = []
overlays = []

def add(renderer):
    standard.append(renderer)

def remove(renderer):
    standard.remove(renderer)
    interrupts.remove(renderer)
    overlays.remove(renderer)

def interrupt(renderer):
    interrupts.append(renderer)

def create_frame():
    return pygame.Surface((width, height))

def create_dots(frame):
    return pygame.PixelArray(frame)

def render():
    global frame, previous
    frame, previous = previous, frame
    if len(interrupts) > 0:
        interrupts[0](frame)
    elif len(standard) > 0:
        standard[-1](frame)
    return frame


