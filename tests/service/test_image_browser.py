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

from mock import Mock, patch
import unittest

from pin.lib import p, resources
from tests import fixtures

class TestImageBrowser(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.browser = p.modes["image_browser"]
        self.browser.enable()

    @patch("pin.lib.resources.load_dmd_animation")
    def test_next(self, patch1):
        previous = self.browser.label.style["text"]
        p.events.post("switch_service_up")
        p.events.dispatch()
        self.assertNotEquals(previous, self.browser.label.style["text"])

    @patch("pin.lib.resources.load_dmd_animation")
    def test_previous(self, patch1):
        previous = self.browser.label.style["text"]
        p.events.post("switch_service_down")
        p.events.dispatch()
        self.assertNotEquals(previous, self.browser.label.style["text"])

    @patch("pin.lib.resources.load_dmd_animation")
    def test_redisplay(self, patch1):
        previous = self.browser.label.style["text"]
        p.events.post("switch_service_enter")
        p.events.dispatch()
        self.assertEquals(previous, self.browser.label.style["text"])

    def test_exit(self):
        p.events.post("switch_service_exit")
        p.events.dispatch()
        self.assertFalse(self.browser.enabled)
