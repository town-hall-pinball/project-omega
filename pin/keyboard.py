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
import pygame.locals

from pin import events

log = logging.getLogger("pin.keyboard")
keys = {}

def process():
    for event in pygame.event.get():
        if event.type == pygame.locals.KEYDOWN:
            name = pygame.key.name(event.key)
            log.debug("down: {}".format(name))
            if name in keys:
                keys[name]["down"]()
        elif event.type == pygame.locals.KEYUP:
            name = pygame.key.name(event.key)
            log.debug("up  : {}".format(name))
            if name in keys:
                keys[name]["up"]()


def event(name, *args, **kwargs):
    def post():
        events.post(name, *args, **kwargs)

    return {
        "down": post,
        "up": lambda : None,
    }

def switch(name, *args, **kwargs):
    def active():
        events.post("switch_{}".format(name))
        events.post("switch_{}_active".format(name))
        events.post("switch_active", name)
        events.post("switch", name, True)

    def inactive():
        events.post("switch_{}_inactive".format(name))
        events.post("switch_inactive", name)
        events.post("switch", name, False)

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




