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

from pin import devices, platform

import p
import unittest
from tests import fixtures
from mock import Mock, patch

class TestDevices(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        platform.devices["SXX"] = 32

    def tearDown(self):
        del platform.devices["SXX"]

    def test_to_string(self):
        self.assertEquals("switch:start_button",
                str(devices.switches["start_button"]))

    def test_disable_switch(self):
        devices.switches["start_button"].disable()

    @patch("p.proc.api")
    def test_disable_coil(self, api):
        devices.coils["trough"].disable()
        self.assertTrue(api.driver_disable.called)

    @patch("p.proc.api")
    def test_disable_coil_2(self, api):
        devices.coils["trough"].enable(False)
        self.assertTrue(api.driver_disable.called)

    def test_duplicate_mapping(self):
        with self.assertRaises(ValueError) as cm:
            devices.add_switches({
                "foo": {
                    "label": "Foo Button",
                    "device": "S13"
                }
            })
        self.assertEquals("switch:foo also maps to switch:start_button",
                str(cm.exception))

    def test_duplicate_device(self):
        with self.assertRaises(ValueError) as cm:
            devices.add_switches({
                "foo": {
                    "label": "Foo Button",
                    "device": "SXX"
                }
            })
        self.assertEquals("Duplicate address number 32 for switch:foo and switch:ball_launch_button",
                str(cm.exception))

    def test_duplicate_name(self):
        devices.reset()
        devices.add_switches({
            "foo": {
                "label": "Foo Button",
                "device": "S13"
            }
        })
        with self.assertRaises(ValueError) as cm:
            devices.add_switches({
                "foo": {
                    "label": "Foo Button",
                    "device": "S14"
                }
            })




