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

from pin.lib import p, engine

import unittest
from mock import Mock, patch
from tests import fixtures


def exit():
    engine.exit = True

class TestEngine(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        engine.reset()

    def tearDown(self):
        engine.reset()

    def test_single_loop(self):
        p1 = Mock()
        engine.processors = [p1, exit]
        engine.run()
        self.assertTrue(p1.called)

    def test_keyboard_interrupt(self):
        p1 = Mock()
        interrupt = Mock(side_effect=KeyboardInterrupt)
        p2 = Mock()
        engine.processors = [p1, interrupt, p2]
        try:
            engine.run()
        except KeyboardInterrupt as ki:
            pass
        self.assertTrue(p1.called)
        self.assertFalse(p2.called)

    def test_metrics_enabled(self):
        p.options["metrics"] = True
        p1 = Mock(side_effect=[1, 2, KeyboardInterrupt])
        engine.processors = [p1]
        try:
            engine.run()
        except KeyboardInterrupt as ki:
            pass
        self.assertTrue(engine.loops > 0)
        self.assertTrue(engine.run_time > 0)

    def test_metrics_disabled(self):
        p.options["metrics"] = False
        p1 = Mock(side_effect=[1, 2, KeyboardInterrupt])
        engine.processors = [p1]
        try:
            engine.run()
        except KeyboardInterrupt as ki:
            pass
        self.assertTrue(engine.loops == 0)
        self.assertTrue(engine.run_time == 0)

    @patch("time.time")
    def test_overrun(self, mock_time):
        p.options["metrics"] = True
        mock_time.side_effect=[0, 1000, 2000]
        engine.processors = [exit]
        engine.run()
        self.assertTrue(engine.overruns > 0)








