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
from pin.lib.util import BallCounter

import unittest
from tests import fixtures
from mock import Mock

class TestBallCounter(unittest.TestCase):

    handler = None
    counter = None

    def setUp(self):
        fixtures.reset()
        self.handler = fixtures.NullHandler()
        self.handler.enable()
        p.switches["trough"].activate()
        fixtures.loop()
        self.counter = BallCounter(self.handler, "trough", [
            p.switches["trough"],
            p.switches["trough_2"],
            p.switches["trough_3"],
            p.switches["trough_4"]
        ])


    def test_initial(self):
        self.assertEquals(1, self.counter.balls)

    def test_enter(self):
        listener = Mock()
        p.events.on("trough_changed", listener)
        p.switches["trough_2"].activate()
        fixtures.loop()
        self.assertEquals(1, self.counter.balls)
        p.now = 1
        fixtures.loop()
        self.assertEquals(2, self.counter.balls)
        self.assertTrue(listener.called)

    def test_exit(self):
        listener = Mock()
        p.events.on("trough_changed", listener)
        p.switches["trough"].deactivate()
        fixtures.loop()
        self.assertEquals(1, self.counter.balls)
        p.now = 1
        fixtures.loop()
        self.assertEquals(0, self.counter.balls)
        self.assertTrue(listener.called)

