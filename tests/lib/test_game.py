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

from pin.lib import p, game

import unittest
from mock import Mock
from tests import fixtures

class TestGame(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.game = game.Game("main")

    def test_initial(self):
        self.assertEquals(0, self.game.ball)
        self.assertFalse(self.game.active)

    def test_start(self):
        listener_start = Mock()
        p.events.on("mode_main", listener_start)
        listener_start_enable = Mock()
        p.events.on("mode_main_enable", listener_start_enable)
        listener_add = Mock()
        p.events.on("add_player", listener_add)
        listener_next = Mock()
        p.events.on("next_player", listener_next)

        self.game.enable()
        p.events.dispatch()
        self.assertEquals(1, self.game.ball)
        self.assertTrue(self.game.active)
        self.assertEquals(1, len(self.game.players))
        self.assertEquals(1, p.player["number"])

        self.assertTrue(listener_start.called)
        self.assertTrue(listener_start_enable.called)
        self.assertTrue(listener_add.called)
        self.assertTrue(listener_next.called)

    def test_add_player(self):
        listener_add = Mock()
        p.events.on("add_player", listener_add)
        self.game.enable()
        self.game.add_player()
        p.events.dispatch()

        self.assertEquals(2, listener_add.call_count)
        self.assertEquals(2, len(p.players))
        self.assertEquals(1, p.player["number"])

    def test_add_player_max(self):
        self.game.enable()
        self.game.add_player()
        self.game.add_player()
        self.game.add_player()
        with self.assertRaises(ValueError):
            self.game.add_player()

    def test_next_player_single(self):
        listener_next = Mock()
        p.events.on("next_player", listener_next)
        self.game.enable()
        self.game.next_player()
        p.events.dispatch()

        self.assertEquals(2, listener_next.call_count)
        self.assertEquals(1, p.player["number"])
        self.assertEquals(2, self.game.ball)

    def test_next_player_multi(self):
        self.game.enable()
        self.game.add_player()
        self.game.next_player()
        p.events.dispatch()

        self.assertEquals(2, p.player["number"])
        self.assertEquals(1, self.game.ball)

    def test_next_player_max(self):
        self.game.enable()
        self.game.add_player()
        self.game.add_player()
        self.game.add_player()
        self.game.next_player()
        self.game.next_player()
        self.game.next_player()
        self.game.next_player()
        p.events.dispatch()

        self.assertEquals(1, p.player["number"])
        self.assertEquals(2, self.game.ball)

    def test_over(self):
        listener_over = Mock()
        p.events.on("game_over", listener_over)

        self.game.enable()
        self.game.next_player()
        self.game.next_player()
        self.game.next_player()
        self.assertFalse(self.game.active)
        self.assertTrue(listener_over.called)


