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

from pin.lib import p, devices
from pin.config import platform

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

    @patch("pin.lib.p.proc.api")
    def test_disable_coil(self, api):
        devices.coils["trough"].disable()
        self.assertTrue(api.driver_disable.called)

    @patch("pin.lib.p.proc.api")
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

    def test_tag(self):
        self.assertTrue("user" in devices.switches["tilt"].tags)
        self.assertFalse("user" in devices.switches["trough"].tags)


class TestDriver(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_default_pulse(self):
        coil = p.coils["trough"]
        listener = Mock()
        def state_listener():
            self.assertEquals(coil.state["schedule"], "pulse")
            self.assertEquals(coil.state["duration"], coil.default_pulse_length)
        p.events.on("coil_trough", listener)
        p.events.on("coil_trough", state_listener)
        coil.pulse()
        self.assertTrue(listener.called)
        self.assertEquals("disable", coil.state["schedule"])

    def test_manual_pulse(self):
        coil = p.coils["trough"]
        listener = Mock()
        def state_listener():
            self.assertEquals(coil.state["schedule"], "pulse")
            self.assertEquals(coil.state["duration"], 100)
        p.events.on("coil_trough", listener)
        p.events.on("coil_trough", state_listener)
        coil.pulse(100)
        self.assertTrue(listener.called)
        self.assertEquals("disable", coil.state["schedule"])

    def test_is_active(self):
        coil = p.coils["trough"]
        coil.patter()
        self.assertTrue(coil.is_active())

    def test_is_not_active(self):
        coil = p.coils["trough"]
        coil.patter()
        coil.disable()
        self.assertFalse(coil.is_active())


class TestCoil(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    # Coverage only
    def test_auto_pulse(self):
        p.coils["kickback"].auto_pulse(p.switches["kickback"])

    def test_auto_pulse_duplicate(self):
        with self.assertRaises(ValueError):
            p.coils["kickback"].auto_pulse(p.switches["kickback"])
            p.coils["kickback"].auto_pulse(p.switches["kickback"])

    # Coverage only
    def test_auto_patter(self):
        p.coils["kickback"].auto_patter(p.switches["kickback"])

    def test_auto_patter_duplicate(self):
        with self.assertRaises(ValueError):
            p.coils["kickback"].auto_patter(p.switches["kickback"])
            p.coils["kickback"].auto_patter(p.switches["kickback"])

    # Coverage only
    def test_auto_cancel(self):
        p.coils["kickback"].auto_pulse(p.switches["kickback"])
        p.coils["kickback"].auto_cancel()

    # Coverage only
    def test_auto_cancel_duplicate(self):
        p.coils["kickback"].auto_pulse(p.switches["kickback"])
        p.coils["kickback"].auto_cancel()
        p.coils["kickback"].auto_cancel()


class TestFlippers(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    # Coverage only
    def test_enable(self):
        p.flippers["left"].auto_pulse()

    # Coverage only
    def test_disable(self):
        p.flippers["left"].auto_cancel()



class TestSwitches(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_elapsed(self):
        p.now = 100
        p.switches["shooter_lane"].activate()
        fixtures.loop()
        p.now = 150
        fixtures.loop()
        self.assertEquals(50, p.switches["shooter_lane"].elapsed())

