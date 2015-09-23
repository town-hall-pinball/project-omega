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

import p
from pin import resources
from tests import fixtures

class TestFontBrowser(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.browser = p.modes["font_browser"]
        self.browser.enable()

    def test_next(self):
        previous = self.browser.label.style["text"]
        p.events.post("switch_service_up")
        p.events.dispatch()
        self.assertNotEquals(previous, self.browser.label.style["text"])

    def test_previous(self):
        previous = self.browser.label.style["text"]
        p.events.post("switch_service_down")
        p.events.dispatch()
        self.assertNotEquals(previous, self.browser.label.style["text"])

    def test_scroll_left(self):
        p.events.post("switch_flipper_left")
        p.events.dispatch()
        p.now = 1
        self.assertFalse(self.browser.scroll_left.running)
        p.timers.service()
        self.assertTrue(self.browser.scroll_left.running)

    def test_scroll_right(self):
        p.events.post("switch_flipper_right")
        p.events.dispatch()
        p.now = 1
        self.assertFalse(self.browser.scroll_right.running)
        p.timers.service()
        self.assertTrue(self.browser.scroll_right.running)

    def test_scroll_left_stop(self):
        self.browser.scroll_left.running = True
        p.events.post("switch_flipper_left_inactive")
        p.events.dispatch()
        self.assertFalse(self.browser.scroll_left.running)

    def test_scroll_right_stop(self):
        self.browser.scroll_right.running = True
        p.events.post("switch_flipper_right_inactive")
        p.events.dispatch()
        self.assertFalse(self.browser.scroll_right.running)

    def test_exit(self):
        p.events.post("switch_service_exit")
        p.events.dispatch()
        self.assertFalse(self.browser.enabled)
