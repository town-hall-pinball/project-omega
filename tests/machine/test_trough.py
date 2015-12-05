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
from mock import Mock

class TestTrough(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.trough = p.modes["trough"]
        self.trough.enable()

    def test_eject(self):
        listener = Mock()
        p.events.on("trough_ejected", listener)
        self.trough.eject()
        p.switches["shooter_lane"].activate()
        fixtures.loop()
        p.now = 0.5
        fixtures.loop()
        self.assertTrue(listener.called)

    def test_disable(self):
        # Coverage only test
        self.trough.disable()

    def test_count_change(self):
        p.switches["trough"].activate()
        fixtures.loop()
        p.now = 1
        fixtures.loop()
        self.assertEquals(1, self.trough.balls)
        p.switches["trough_2"].activate()
        fixtures.loop()
        p.now = 2
        fixtures.loop()
        self.assertEquals(2, self.trough.balls)


