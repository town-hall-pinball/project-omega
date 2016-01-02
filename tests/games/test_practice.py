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
from mock import patch

class TestPractice(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.mode = p.modes["practice"]
        p.modes["simulator"].enable()
        p.modes["practice"].enable()

    def test_saucer_disable_magnets(self):
        p.switches["ball_launch_button"].activate()
        fixtures.loop()
        p.switches["saucer"].activate()
        fixtures.loop()
        p.now = 1.0
        fixtures.loop()
        self.assertFalse(self.mode.magnets)

    def test_saucer_reenable_magnets(self):
        p.switches["ball_launch_button"].activate()
        fixtures.loop()
        p.switches["saucer"].activate()
        fixtures.loop()
        p.now = 1.0
        fixtures.loop()
        self.assertFalse(self.mode.magnets)

        p.now = 2.0
        fixtures.loop()
        p.switches["saucer"].deactivate()
        p.now = 3.0
        fixtures.loop()

        p.now = 4.0
        p.switches["saucer"].activate()
        fixtures.loop()
        p.now = 5.0
        fixtures.loop()
        self.assertTrue(self.mode.magnets)

    def test_time_display(self):
        fixtures.launch()
        self.assertEquals("3:00", self.mode.time.style["text"])
        p.now += 2
        fixtures.loop()
        self.assertEquals("2:58", self.mode.time.style["text"])

    def test_game_end(self):
        fixtures.launch()
        self.assertTrue(p.modes["flippers"].enabled)
        p.now += 3 * 60.0
        fixtures.loop()
        self.assertFalse(p.modes["flippers"].enabled)
        fixtures.drain()
        self.assertFalse(p.game)


