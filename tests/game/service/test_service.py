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
from tests import fixtures

class TestService(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.service = p.modes["service"]
        self.service.enable()

    def test_menu_next(self):
        p.events.post("switch_service_up")
        p.events.dispatch()
        self.assertEquals("Tests", self.service.name.style["text"])

    def test_menu_previous(self):
        p.events.post("switch_service_down")
        p.events.dispatch()
        self.assertEquals("Utilities", self.service.name.style["text"])

    def test_menu_exit(self):
        p.events.post("switch_service_exit")
        p.events.dispatch()
        self.assertFalse(self.service.enabled)

    def test_menu_down(self):
        p.events.post("switch_service_enter")
        p.events.dispatch()
        self.assertEquals("Pricing", self.service.name.style["text"])

    def test_option_select(self):
        p.events.post("switch_service_enter")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_up")
        p.events.post("switch_service_enter")
        p.events.dispatch()
        self.assertEquals("1 for 0.25", self.service.value.style["text"])

    def test_option_select_next(self):
        p.events.post("switch_service_enter")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_up")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_up")
        p.events.dispatch()
        self.assertEquals("1 for 0.50", self.service.value.style["text"])

    def test_option_select_previous(self):
        p.events.post("switch_service_enter")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_up")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_down")
        p.events.dispatch()
        self.assertEquals("1 for 1.00", self.service.value.style["text"])

    def test_data_display(self):
        p.data["earnings"] = 1.23
        p.events.post("switch_service_up") # Tests
        p.events.post("switch_service_up") # Audits
        p.events.post("switch_service_enter") # Enter Audtis
        p.events.dispatch()
        self.assertEquals("1.23", self.service.value.style["text"])

    def test_confirm_action(self):
        p.data["credits"] = 10
        p.events.post("switch_service_down") # Utilities
        p.events.post("switch_service_enter") # Enter Utilities
        p.events.post("switch_service_up") # Clear
        p.events.post("switch_service_enter") # Enter Clear
        p.events.post("switch_service_enter") # Clear Credits
        p.events.post("switch_service_up") # Move to YES
        p.events.post("switch_service_enter") # Confirm
        p.events.dispatch()
        self.assertEquals(0, p.data["credits"])

    def test_confirm_action_previous(self):
        p.data["credits"] = 10
        p.events.post("switch_service_down") # Utilities
        p.events.post("switch_service_enter") # Enter Utilities
        p.events.post("switch_service_up") # Clear
        p.events.post("switch_service_enter") # Enter Clear
        p.events.post("switch_service_enter") # Clear Credits
        p.events.post("switch_service_down") # Move to YES
        p.events.post("switch_service_enter") # Confirm
        p.events.dispatch()
        self.assertEquals(0, p.data["credits"])

    def test_cancel_action(self):
        p.data["credits"] = 10
        p.events.post("switch_service_down") # Utilities
        p.events.post("switch_service_enter") # Enter Utilities
        p.events.post("switch_service_up") # Clear
        p.events.post("switch_service_enter") # Enter Clear
        p.events.post("switch_service_enter") # Clear Credits
        p.events.post("switch_service_enter") # Select NO
        p.events.dispatch()
        self.assertEquals(10, p.data["credits"])

    def test_save(self):
        p.data["free_play"] = False
        p.events.post("switch_service_enter") # Enter Settings
        p.events.post("switch_service_enter") # Enter Pricing
        p.events.post("switch_service_enter") # Enter Free Play
        p.events.post("switch_service_up") # Select YES
        p.events.post("switch_service_enter") # Save
        p.events.dispatch()
        self.assertTrue(p.data["free_play"])

    def test_no_chace(self):
        p.data["free_play"] = False
        p.events.post("switch_service_enter") # Enter Settings
        p.events.post("switch_service_enter") # Enter Pricing
        p.events.post("switch_service_enter") # Enter Free Play
        p.events.post("switch_service_enter") # No Change
        p.events.dispatch()
        self.assertFalse(p.data["free_play"])
