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

from pin.lib import p

import unittest
from tests import fixtures
from mock import patch, Mock

class TestPractice(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.mode = p.modes["practice"]
        p.modes["simulator"].enable()
        p.modes["practice"].enable()

    def test_saucer_disable_magnets(self):
        fixtures.launch()
        #p.switches["ball_launch_button"].activate()
        #fixtures.loop()
        p.switches["saucer"].activate()
        fixtures.loop("saucer")
        p.now += 1.0
        fixtures.loop("saucer_eject")
        self.assertFalse(self.mode.magnets)

    def test_saucer_reenable_magnets(self):
        #p.switches["ball_launch_button"].activate()
        #fixtures.loop()
        fixtures.launch()
        p.switches["saucer"].activate()
        fixtures.loop()
        p.now += 1.0
        fixtures.loop()
        self.assertFalse(self.mode.magnets)

        p.now += 1.0
        fixtures.loop()
        p.switches["saucer"].deactivate()
        p.now += 1.0
        fixtures.loop()

        p.now += 1.0
        p.switches["saucer"].activate()
        fixtures.loop()
        p.now += 1.0
        fixtures.loop()
        self.assertTrue(self.mode.magnets)

    def test_time_display(self):
        fixtures.launch()
        self.assertEquals("3:00", self.mode.time.style["text"])
        p.now += 2
        fixtures.loop()
        self.assertEquals("2:58", self.mode.time.style["text"])

    def test_popper(self):
        listener = Mock()
        p.events.on("coil_popper", listener)
        fixtures.launch()
        p.events.post("switch_subway_center")
        fixtures.loop()
        p.now += 1
        fixtures.loop()
        self.assertTrue(listener.called)

    def test_drop_target_up(self):
        p.modes["drop_target"].down()
        fixtures.loop()
        fixtures.launch()
        listener = Mock()
        p.events.on("coil_drop_target_up", listener)
        p.switches["subway_left"].activate()
        fixtures.loop()
        self.assertTrue(listener.called)

    def test_launch_after_drain(self):
        fixtures.launch()
        listener = Mock()
        p.events.on("coil_auto_plunger", listener)
        p.switches["trough_4"].activate()
        fixtures.loop()
        p.now += 1
        fixtures.loop()
        self.assertTrue(listener.called)

    def test_no_launch_after_tilted_drain(self):
        fixtures.launch()
        listener = Mock()
        p.events.on("coil_auto_plunger", listener)
        p.modes["practice"].tilted = True
        p.switches["trough_4"].activate()
        fixtures.loop()
        p.now += 1
        fixtures.loop()
        self.assertFalse(listener.called)

    def test_tilt(self):
        fixtures.launch()
        self.assertTrue(p.modes["practice"].ticker)
        p.modes["practice"].tilt()
        self.assertFalse(p.modes["practice"].ticker)

    def test_game_end(self):
        fixtures.launch()
        self.assertTrue(p.modes["flippers"].enabled)
        p.now += 3 * 60.0
        fixtures.loop()
        self.assertFalse(p.modes["flippers"].enabled)
        fixtures.drain()
        self.assertFalse(p.game)


