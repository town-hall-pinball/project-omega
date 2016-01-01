# Copyright (c) 2014 - 2016 townhallpinball.org
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
from pin.lib import p, resources, util

import unittest
from tests import fixtures
from mock import Mock

class TestMixer(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        p.sounds["sound_1"] = pygame.mixer.Sound()
        p.music["music_1"] = resources.Music("/tmp/music_1")

    def test_create_master_channel(self):
        self.assertEquals(0, len(p.mixer.channels))
        p.mixer.play("sound_1")
        self.assertTrue("master" in p.mixer.channels)

    def test_create_other_channel(self):
        p.mixer.play("sound_1", channel="other")
        self.assertTrue("other" in p.mixer.channels)

    def test_play_sound(self):
        p.mixer.play("sound_1")
        self.assertTrue(p.mixer.channels["master"].play.called)

    def test_play_sound_quiet(self):
        p.options["quiet"] = True
        p.mixer.play("sound_1")
        self.assertFalse(p.mixer.channels["master"].play.called)

    def test_play_music(self):
        p.mixer.play("music_1")
        pygame.mixer.music.load.assert_called_with("/tmp/music_1")

    def test_stop_sound_channel(self):
        p.mixer.play("sound_1", channel="other")
        p.mixer.stop("other")
        self.assertTrue(p.mixer.channels["other"].stop.called)

    def test_stop_music(self):
        p.mixer.play("music_1")
        p.mixer.stop("music")
        self.assertTrue(pygame.mixer.music.stop.called)

    def test_stop_all(self):
        p.mixer.play("music_1")
        p.mixer.play("sound_1", channel="other")
        p.mixer.stop()
        self.assertTrue(p.mixer.channels["other"].stop.called)
        self.assertTrue(pygame.mixer.music.stop.called)

