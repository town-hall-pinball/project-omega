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
from pin import timers

import unittest
from mock import Mock
from tests import fixtures

class TestTimers(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        timers.reset()

    def test_set_called(self):
        callback = Mock()
        timers.set(1.0, callback)
        p.now = 2.0
        timers.service()
        self.assertTrue(callback.called)

    def test_set_not_called(self):
        callback = Mock()
        timers.set(1.0, callback)
        p.now = 0.5
        timers.service()
        self.assertFalse(callback.called)

    def test_set_not_called_twice(self):
        callback = Mock()
        timers.set(1.0, callback)
        p.now = 2.0
        timers.service()
        self.assertEquals(1, callback.call_count)
        p.now = 3.0
        timers.service()
        self.assertEquals(1, callback.call_count)

    def test_clear(self):
        callback = Mock()
        ident1 = timers.set(1.0, callback)
        ident2 = timers.tick(callback)
        timers.clear(ident1)
        timers.clear(ident2)
        p.now = 2.0
        timers.service()
        self.assertFalse(callback.called)

    def test_tick(self):
        callback = Mock()
        timers.tick(callback)
        timers.service()
        timers.service()
        self.assertEquals(2, callback.call_count)
