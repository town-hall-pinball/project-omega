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

import itertools
import logging
import pygame
import p

log = logging.getLogger("pin.mixer")

channels = {}
ident = itertools.count(0)

def play(sound_name, channel="master", duration=0):
    if sound_name in p.music:
        log.debug("music: Playing {}".format(sound_name))
        music = p.music[sound_name]
        if not p.options["quiet"]:
            pygame.mixer.music.load(music.path)
            pygame.mixer.music.play(0, music.start_time)
    else:
        if channel not in channels:
            log.debug("Creating mixer channel: {}".format(channel))
            channels[channel] = pygame.mixer.Channel(ident.next())
        sound = p.sounds[sound_name]
        log.debug("{}: Playing {}".format(channel, sound_name))
        if not p.options["quiet"]:
            channels[channel].play(sound, maxtime=int(duration * 1000))

def stop(channel=None):
    if channel is None:
        for channel in channels.values():
            channel.stop()
        pygame.mixer.music.stop()
    elif channel in channels:
        channels[channel].stop()
    else:
        pygame.mixser.music.stop()

