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

from mock import Mock
import unittest

from pin.util import Events

class TestEvents(unittest.TestCase):

    def setUp(self):
        self.events = Events()

    def test_on(self):
        listener = Mock()
        self.events.on("foo", listener)
        self.events.post("foo")
        self.events.dispatch()
        self.assertTrue(listener.called)

    def test_off(self):
        listener = Mock()
        self.events.on("foo", listener)
        self.events.post("foo")
        self.events.dispatch()
        self.events.off("foo", listener)
        self.events.post("foo")
        self.events.dispatch()
        self.assertEquals(1, listener.call_count)

    def test_multiple_dispatch(self):
        listener1 = Mock()
        listener2 = Mock()
        self.events.on("foo", listener1)
        self.events.on("foo", listener2)
        self.events.post("foo")
        self.events.dispatch()
        self.assertTrue(listener1.called)
        self.assertTrue(listener2.called)

    def test_arguments(self):
        listener = Mock()
        self.events.on("foo", listener)
        self.events.post("foo", 1, bar=2)
        self.events.dispatch()
        listener.assert_called_with(1, bar=2)


