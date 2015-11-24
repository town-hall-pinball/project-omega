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

from pin import config
from pin.lib import (
    p, dmd, devices, events, keyboard, resources, mixer, proc, shots,
    timers
)
from pin.lib.data import data
from pin.config import default, platform, startup
from pin.lib.virtual import proc as virtual_proc
from mock import MagicMock as Mock, patch
import pygame

def reset():
    p.defaults = default.settings

    keyboard.reset()
    events.reset()
    timers.reset()
    #shots.reset()

    p.dmd = dmd
    p.data = data
    p.events = events
    p.fonts = resources.fonts
    p.game = None
    p.images = resources.images
    p.mixer = mixer
    p.music = resources.music
    p.movies = resources.movies
    p.now = 0
    p.platform = platform
    p.proc = proc
    p.proc.api = virtual_proc
    p.sounds = resources.sounds
    p.switches = devices.switches
    p.timers = timers

    p.proc.api.dmd_enabled = False
    p.data.reset(p.defaults)
    p.data.read_only = True

    p.options = {
        "fast": False,
        "font": None,
        "image": None,
        "movie": None,
        "music": None,
        "sound": None,
        "virtual": False,
        "quiet": False,
    }

    p.mixer.reset()
    devices.reset()
    resources.reset()
    p.proc.reset()
    p.dmd.reset()

    pygame.mixer.Sound = Mock(pygame.mixer.Sound)
    pygame.mixer.Channel = Mock(pygame.mixer.Channel)
    pygame.font.Font = Mock(pygame.font.Font)
    pygame.mixer.music = Mock(pygame.mixer.music)
    pygame.key.get_mods = Mock()
    pygame.key.get_mods.return_value = 0

    movie = Mock(spec=[
        "get_size",
        "play",
        "rewind",
        "set_display",
        "stop",
    ])
    pygame.movie.Movie = Mock()
    pygame.movie.Movie.return_value = movie
    movie.get_size.return_value = (128, 32)

    font = pygame.font.Font.return_value
    font.metrics.return_value = ((5, 5, 5, 5, 5),)
    font.get_ascent.return_value = 5

    config.init()
    with patch("pin.lib.resources.load_dmd_animation") as load_patch:
        startup.init()

    p.modes["shots"].enable()


class LoopError(Exception):
    pass

def loop():
    with patch("pin.lib.p.proc.api.get_events") as get_events:
        get_events.return_value = []
        done = False
        loops = 0
        while not done:
            if loops > 100:
                raise LoopError()
            p.events.dispatch()
            p.proc.process()
            p.timers.service()
            if len(p.events.queue) == 0:
                done = True
            loops += 1


