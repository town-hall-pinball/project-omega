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

from mock import Mock, patch
import unittest

from pin.lib import p
from tests import fixtures

class TestService(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.service = p.modes["service"]
        self.service.enable()

    def test_menu_next(self):
        p.events.post("switch_service_up")
        p.events.dispatch()
        self.assertEquals("Tests", self.service.title.style["text"])

    def test_menu_previous(self):
        p.events.post("switch_service_down")
        p.events.dispatch()
        self.assertEquals("Utilities", self.service.title.style["text"])

    def test_menu_next_suspended(self):
        self.service.suspend()
        p.events.post("switch_service_up")
        p.events.dispatch()
        self.assertEquals("Settings", self.service.title.style["text"])
        self.service.resume()
        p.events.post("switch_service_up")
        p.events.dispatch()
        self.assertEquals("Tests", self.service.title.style["text"])

    def test_menu_exit(self):
        p.events.post("switch_service_exit")
        p.events.dispatch()
        self.assertFalse(self.service.enabled)

    def test_menu_down(self):
        p.events.post("switch_service_enter")
        p.events.dispatch()
        self.assertEquals("Pricing", self.service.title.style["text"])

    def test_menu_cache(self):
        p.events.post("switch_service_up")      # Go to Tests
        p.events.post("switch_service_enter")   # Enter Tests
        p.events.post("switch_service_up")      # Go to Coils
        p.events.post("switch_service_exit")    # Back to main
        p.events.post("switch_service_enter")   # Enter Tests
        p.events.dispatch()
        self.assertEquals("Coils", self.service.title.style["text"])

    def test_option_select(self):
        p.events.post("switch_service_enter")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_up")
        p.events.post("switch_service_enter")
        p.events.dispatch()
        self.assertEquals("1 for 0.50", self.service.value.style["text"])

    def test_option_select_next(self):
        p.events.post("switch_service_enter")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_up")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_up")
        p.events.dispatch()
        self.assertEquals("1 for 0.75", self.service.value.style["text"])

    def test_option_select_previous(self):
        p.events.post("switch_service_enter")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_up")
        p.events.post("switch_service_enter")
        p.events.post("switch_service_down")
        p.events.dispatch()
        self.assertEquals("1 for 0.25", self.service.value.style["text"])

    def test_data_display(self):
        p.data["earnings"] = 1.23
        p.events.post("switch_service_up") # Tests
        p.events.post("switch_service_up") # Audits
        p.events.post("switch_service_enter") # Enter Audtis
        p.events.dispatch()
        self.assertEquals("1.23", self.service.value.style["text"])

    def test_action(self):
        p.events.post("switch_service_down")    # To Utilities
        p.events.post("switch_service_enter")   # Enter Utilities
        p.events.post("switch_service_down")    # To More...
        p.events.post("switch_service_down")    # To Debug
        p.events.post("switch_service_down")    # To Browsers
        p.events.post("switch_service_enter")   # Enter Browsers
        p.events.post("switch_service_enter")   # Select Music Browser
        p.events.dispatch()
        self.assertTrue(p.modes["music_browser"].enabled)

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

    def test_cancel_exit(self):
        p.data["credits"] = 10
        p.events.post("switch_service_down") # Utilities
        p.events.post("switch_service_enter") # Enter Utilities
        p.events.post("switch_service_up") # Clear
        p.events.post("switch_service_enter") # Enter Clear
        p.events.post("switch_service_enter") # Clear Credits
        p.events.post("switch_service_exit") # Exit out
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
        p.now = 5                             # Remove confirmation message
        p.timers.service()

    def test_no_change(self):
        p.data["free_play"] = False
        p.events.post("switch_service_enter") # Enter Settings
        p.events.post("switch_service_enter") # Enter Pricing
        p.events.post("switch_service_enter") # Enter Free Play
        p.events.post("switch_service_enter") # No Change
        p.events.dispatch()
        self.assertFalse(p.data["free_play"])


class TestServiceActions(unittest.TestCase):

    def setUp(self):
        self.service = p.modes["service"]
        self.service.enable()

    def test_clear_credits(self):
        p.data["credits"] = 5
        self.service.clear_credits()
        self.assertEquals(0, p.data["credits"])

    def test_movie_browser(self):
        self.service.movie_browser()
        self.assertTrue(p.modes["movie_browser"].enabled)

    def test_music_browser(self):
        self.service.music_browser()
        self.assertTrue(p.modes["music_browser"].enabled)

    def test_sound_browser(self):
        self.service.sound_browser()
        self.assertTrue(p.modes["sound_browser"].enabled)

    def test_font_browser(self):
        self.service.font_browser()
        self.assertTrue(p.modes["font_browser"].enabled)

    def test_image_browser(self):
        self.service.image_browser()
        self.assertTrue(p.modes["image_browser"].enabled)



