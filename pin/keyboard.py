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

import logging
import pygame
from pygame.locals import *

import p

log = logging.getLogger("pin.keyboard")
keys = {}

def mod():
    keys = []
    m = pygame.key.get_mods()
    if m & KMOD_LSHIFT or m & KMOD_RSHIFT:
        keys += ["s"]
    return "".join(keys)

def process():
    for event in pygame.event.get():
        if event.type == KEYDOWN or event.type == KEYUP:
            name = pygame.key.name(event.key)
            key = mod() + name
            if event.type == KEYDOWN:
                log.debug("down: {}".format(name))
                if key in keys:
                    keys[key]["down"]()
            elif event.type == KEYUP:
                log.debug("up  : {}".format(name))
                if key in keys:
                    keys[key]["up"]()


def event(name, *args, **kwargs):
    def post():
        p.events.post(name, *args, **kwargs)

    return {
        "down": post,
        "up": lambda : None,
    }

def switch(name, *args, **kwargs):
    switch = p.switches[name]

    def active():
        event = p.proc.SWITCH_OPENED if switch.opto else p.proc.SWITCH_CLOSED
        p.proc.artificial_events += [{"type": event, "value": switch.number}]

    def inactive():
        event = p.proc.SWITCH_CLOSED if switch.opto else p.proc.SWITCH_OPENED
        p.proc.artificial_events += [{"type": event, "value": switch.number}]

    return {
        "down": active,
        "up": inactive
    }

def register(config):
    for key, function in config.items():
        if key in keys:
            raise ValueError("Duplicate key mapping: {}".format(key))
        keys[key] = function

def reset():
    keys.clear()




