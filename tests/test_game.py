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
from pin.game import Game

import unittest
from mock import Mock
from tests import fixtures

class TestGame(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.game = Game("main")

    def test_initial(self):
        self.assertEquals(0, self.game.ball)
        self.assertFalse(self.game.active)

    def test_start(self):
        listener1 = Mock()
        p.events.on("game_start", listener1)
        listener2 = Mock()
        p.events.on("game_start_main", listener2)

        self.game.start()
        p.events.dispatch()
        self.assertEquals(1, self.game.ball)
        self.assertTrue(self.game.active)
        self.assertEquals(1, len(self.game.players))
        self.assertEquals(1, p.player["number"])
        listener1.assert_called_with("main")
        self.assertTrue(listener2.called)



