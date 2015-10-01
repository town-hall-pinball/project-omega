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

from pin.lib import p, util
import unittest
from mock import Mock
from tests import fixtures

class TestShow(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_single_run(self):
        action = Mock()
        callback = Mock()
        show = util.Show("show", [1, 1], action=action, callback=callback)
        show.start()
        p.timers.service()
        for now in xrange(0, 4):
            p.now = now
            p.timers.service()
        self.assertEquals(2, action.call_count)
        self.assertFalse(show.running)
        self.assertTrue(callback.called)

    def test_repeat_twice(self):
        action = Mock()
        callback = Mock()
        show = util.Show("show", [1, 1], action=action, repeat=2,
                callback=callback)
        show.start()
        for now in xrange(0, 6):
            p.now = now
            p.timers.service()
        self.assertEquals(4, action.call_count)
        self.assertFalse(show.running)
        self.assertTrue(callback.called)

    def test_repeat_always(self):
        action = Mock()
        callback = Mock()
        show = util.Show("show", [1, 1], action=action, repeat=True,
                callback=callback)
        show.start()
        for now in xrange(0, 6):
            p.now = now
            p.timers.service()
        self.assertEquals(6, action.call_count)
        self.assertTrue(show.running)
        self.assertFalse(callback.called)

