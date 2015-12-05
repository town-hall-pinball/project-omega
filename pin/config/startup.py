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

from pin.lib import p
from . import keyboard, service_menu, resources
from .. import extra

# Resources now in resources.py

def init(load_resources=True):
    p.service_menu = service_menu

    if load_resources:
        resources.load()
        extra.load()

    p.load_modes((
        "lib.ball",
        "lib.server",
        "lib.simulator",

        "system.coin",
        "system.attract",
        "system.banner",
        "system.core",
        "system.game_menu",
        "system.pinball_missing",
        "system.post",

        "machine.drop_target",
        "machine.flippers",
        "machine.kickback",
        "machine.magnets",
        "machine.plunger",
        "machine.popper",
        "machine.saucer",
        "machine.slingshots",
        "machine.trough",

        "service.coils_test",
        "service.flashers_all_test",
        "service.flashers_single_test",
        "service.flippers_test",
        "service.font_browser",
        "service.image_browser",
        "service.lamps_all_test",
        "service.lamps_single_test",
        "service.movie_browser",
        "service.music_browser",
        "service.sound_browser",
        "service.switch_edges_test",
        "service.switch_levels_test",
        "service.switch_single_test",
        "service.virtual_palette",
        "service.service",

        "games.practice",
    ))
    extra.init()
    keyboard.init()

def bootstrap():
    for gi in p.gi.values():
        gi.enable()

    if not p.modes["service"].direct_start():
        if p.options["fast"]:
            p.modes["core"].enable()
            p.modes["attract"].enable()
        else:
            p.modes["post"].enable()
