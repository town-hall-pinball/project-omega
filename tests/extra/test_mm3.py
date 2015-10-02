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
import unittest
from tests import fixtures
from mock import patch

class TestMM3(unittest.TestCase):

    def setUp(self):
        with patch("pin.lib.resources.available") as mock_available:
            mock_available.return_value = True
            fixtures.reset()
            self.mm3 = p.modes["mm3"]
            self.mm3.enable()

    def test_next(self):
        boss = self.mm3.stage_select.boss
        self.assertEquals("mm3_spark_man", boss.style["image"])
        p.events.post("switch_flipper_right")
        p.events.dispatch()
        self.assertEquals("mm3_snake_man", boss.style["image"])

    def test_previous(self):
        boss = self.mm3.stage_select.boss
        self.assertEquals("mm3_spark_man", boss.style["image"])
        p.events.post("switch_flipper_left")
        p.events.dispatch()
        self.assertEquals("mm3_shadow_man", boss.style["image"])

    def test_select(self):
        p.events.post("switch_start_button")
        p.events.dispatch()
        self.assertTrue(self.mm3.game_start.enabled)
        p.now = 0
        p.timers.service()
        p.now += 1.75 # tear_end
        p.timers.service()
        p.now += 1.50 # blend_out
        p.timers.service()
        p.now += 1.75 # typewriter
        p.timers.service()
        p.now = 100
        p.timers.service()
        self.assertFalse(self.mm3.game_start.enabled)

    def test_timeout(self):
        p.now = 100
        p.timers.service()
        self.assertFalse(self.mm3.enabled)
        self.assertTrue(p.modes["attract"].enabled)

    def test_timeout_restart(self):
        # fixes #6: Listener already registered for switch_start_button
        p.now = 100
        p.timers.service()
        self.mm3.enable()

    @patch("pin.lib.resources.available")
    def test_no_init(self, mock_available):
        mock_available.return_value = False
        from pin.extra import mm3
        self.assertEquals(False, mm3.init())
        self.assertEquals(False, mm3.load())



