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

import p

from .config import defaults, keyboard, resources
from . import extra

# Resources now in resources.py

def init(load_resources=True):
    if load_resources:
        resources.load()
        extra.load()

    p.load_modes((
        "server",
        "simulator",
        "game.main.score",
        "game.system",
        "game.attract",
        "game.banner",
        "game.post",
        "game.starter",
        "game.service.coils_test",
        "game.service.flashers_all_test",
        "game.service.flashers_single_test",
        "game.service.font_browser",
        "game.service.image_browser",
        "game.service.lamps_all_test",
        "game.service.lamps_single_test",
        "game.service.movie_browser",
        "game.service.music_browser",
        "game.service.sound_browser",
        "game.service.switch_edges_test",
        "game.service.switch_levels_test",
        "game.service.switch_single_test",
        "game.service.service",
    ))
    extra.init()
    keyboard.init()

def start():
    for gi in p.gi.values():
        gi.enable()

    if not p.modes["service"].direct_start():
        if p.options["fast"]:
            p.modes["system"].enable()
            p.modes["attract"].enable()
        else:
            p.modes["post"].enable()
