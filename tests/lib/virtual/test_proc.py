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

class TestPROC(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_reset(self):
        p.proc.api.reset()

    def test_get_events(self):
        p.proc.api.dmd_enabled = True
        events = p.proc.api.get_events()
        self.assertEquals(1, len(events))
        self.assertEquals(p.proc.DMD_READY, events[0]["type"])

    def test_switch_update_rule(self):
        p.proc.api.switch_update_rule()

    def test_flush(self):
        p.proc.api.flush()

    def test_watchdog_tickle(self):
        p.proc.api.watchdog_tickle()

    def test_dmd_draw(self):
        p.proc.api.dmd_draw()

    def test_driver_pulse(self):
        p.proc.api.driver_pulse()

    def test_driver_disable(self):
        p.proc.api.driver_disable()

