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

import unittest
from tests import fixtures
from mock import patch

class TestAttract(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.attract = p.modes["attract"]
        self.attract.enable()

    @patch("p.mixer.stop")
    def test_disable(self, mixer_stop):
        self.attract.disable()
        self.assertTrue(mixer_stop.called)

    def test_suspend(self):
        self.attract.suspend()
        self.assertFalse(self.attract.show.running)

    def test_resume(self):
        self.attract.suspend()
        self.attract.resume()
        self.assertTrue(self.attract.show.running)

    def test_start_service_mode(self):
        p.events.post("switch_service_enter")
        p.events.dispatch()
        self.assertFalse(self.attract.enabled)
        self.assertTrue(p.modes["service"].enabled)


