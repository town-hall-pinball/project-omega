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
import pin
from pin.game.config.defaults import defaults
from pin.virtual import proc as virtual_proc
from mock import Mock
import pygame

def reset():
    from pin.platforms import wpc as platform
    from pin.machines import no_fear as machine

    p.platform = platform
    p.machine = machine
    p.defaults = defaults

    pin.keyboard.reset()
    pin.events.reset()

    p.dmd = pin.dmd
    p.data = pin.data
    p.events = pin.events
    p.fonts = pin.resources.fonts
    p.images = pin.resources.images
    p.mixer = pin.mixer
    p.music = pin.resources.music
    p.movies = pin.resources.movies
    p.now = 0
    p.proc = pin.proc
    p.proc.api = virtual_proc
    p.sounds = pin.resources.sounds
    p.switches = pin.devices.switches
    p.timers = pin.timers

    p.data.reset(p.defaults)

    p.options = {
        "fast": False,
        "virtual": False,
        "quiet": False,
    }

    pin.devices.reset()
    machine.init()

    pygame.mixer.Sound = Mock(pygame.mixer.Sound)
    pygame.mixer.Channel = Mock(pygame.mixer.Channel)
    pygame.font.Font = Mock(pygame.font.Font)
    pygame.movie.Movie = Mock(pygame.movie.Movie)

    font = pygame.font.Font.return_value
    font.metrics.return_value = ((5, 5, 5, 5, 5),)
    font.get_ascent.return_value = 5


