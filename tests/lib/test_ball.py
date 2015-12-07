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

from pin.lib import p, ball

import unittest
from mock import Mock
from tests import fixtures


class TestSearch(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        ball.search_sequence = [
            p.coils["saucer"],
            p.coils["popper"]
        ]

    def test_search(self):
        listener1 = Mock()
        listener2 = Mock()
        p.events.on("coil_saucer", listener1)
        p.events.on("coil_popper", listener2)
        ball.search()
        fixtures.loop()
        self.assertTrue(listener1.called)
        p.now += ball.search_interval
        fixtures.loop()
        self.assertTrue(listener2.called)
        self.assertFalse(ball.search.running)

    def test_search_already_running(self):
        listener1 = Mock()
        listener2 = Mock()
        p.events.on("coil_saucer", listener1)
        p.events.on("coil_popper", listener2)
        ball.search()
        fixtures.loop()
        ball.search()
        self.assertTrue(listener1.called)
        self.assertFalse(listener2.called)
        self.assertTrue(ball.search.running)





