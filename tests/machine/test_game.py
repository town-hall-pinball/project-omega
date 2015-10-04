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
from pin.machine.game import Game

import unittest
from tests import fixtures

class TestGame(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.game = Game()

    def test_kickback_enable(self):
        self.game.kickback_enable()
        self.assertTrue(self.game.kickback_enabled)
        self.assertTrue(p.coils["kickback"].auto_switch_name)

    def test_kickback_disable(self):
        self.game.kickback_enable()
        self.game.kickback_disable()
        self.assertFalse(self.game.kickback_enabled)
        self.assertFalse(p.coils["kickback"].auto_switch_name)

    def test_magnets_assist(self):
        self.game.magnets_assist()
        self.assertEquals(self.game.magnets_enabled, "assist")
        self.assertTrue(p.coils["magnet_left"].auto_switch_name)
        self.assertTrue(p.coils["magnet_center"].auto_switch_name)
        self.assertTrue(p.coils["magnet_right"].auto_switch_name)

    def test_magnets_disable(self):
        self.game.magnets_assist()
        self.game.magnets_disable()
        self.assertFalse(self.game.magnets_enabled)
        self.assertFalse(p.coils["magnet_left"].auto_switch_name)
        self.assertFalse(p.coils["magnet_center"].auto_switch_name)
        self.assertFalse(p.coils["magnet_right"].auto_switch_name)

    def test_flippers_enable(self):
        self.game.flippers_enable()
        self.assertTrue(self.game.flippers_enabled)
        self.assertTrue(p.flippers["left"].auto_switch_name)
        self.assertTrue(p.flippers["right"].auto_switch_name)
        self.assertFalse(p.flippers["right_up"].auto_switch_name)

    def test_loop_enable(self):
        self.game.loop_enable()
        self.assertTrue(self.game.loop_enabled)
        self.assertTrue(p.flippers["right_up"].auto_switch_name)

    def test_loop_disable(self):
        self.game.loop_disable()
        self.assertFalse(self.game.loop_enabled)
        self.assertFalse(p.flippers["right_up"].auto_switch_name)

    def test_flippers_disable(self):
        self.game.flippers_enable()
        self.game.loop_enable()
        self.game.flippers_disable()
        self.assertFalse(self.game.flippers_enabled)
        self.assertFalse(self.game.loop_enabled)
        self.assertFalse(p.flippers["left"].auto_switch_name)
        self.assertFalse(p.flippers["right"].auto_switch_name)
        self.assertFalse(p.flippers["right_up"].auto_switch_name)

    def test_playfield_enable(self):
        self.game.playfield_enable()
        self.assertTrue(self.game.flippers_enabled)
        self.assertTrue(self.game.playfield_enabled)
        self.assertTrue(p.coils["slingshot_left"].auto_switch_name)
        self.assertTrue(p.coils["slingshot_right"].auto_switch_name)

    def test_playfield_disable(self):
        self.game.playfield_enable()
        self.game.loop_enable()
        self.game.kickback_enable()
        self.game.playfield_disable()
        self.assertFalse(self.game.flippers_enabled)
        self.assertFalse(self.game.loop_enabled)
        self.assertFalse(self.game.kickback_enabled)
        self.assertFalse(self.game.playfield_enabled)
        self.assertFalse(p.coils["slingshot_left"].auto_switch_name)
        self.assertFalse(p.coils["slingshot_right"].auto_switch_name)


