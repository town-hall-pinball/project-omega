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
import pin

import unittest
from mock import Mock, patch
from tests import fixtures

class TestPROC(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    @patch("pin.proc.create_buffer")
    def test_init(self, *args):
        pin.proc.init()

    @patch("pygame.PixelArray")
    def test_process(self, *args):
        p.dmd.render = Mock()
        pin.proc.process()

    @patch("pygame.PixelArray")
    def test_active_switch_event(self, *args):
        p.dmd.render = Mock()
        get_events = Mock()
        switch = p.switches["start_button"]
        get_events.return_value = [{
            "type": p.proc.SWITCH_CLOSED,
            "value": switch.number
        }]
        p.proc.api.get_events = get_events

        listener1 = Mock()
        listener2 = Mock()
        listener3 = Mock()
        listener4 = Mock()

        p.events.on("switch_start_button", listener1)
        p.events.on("switch_start_button_active", listener2)
        p.events.on("switch_active", listener3)
        p.events.on("switch", listener4)

        pin.proc.process()
        p.events.dispatch()

        self.assertTrue(listener1.called)
        self.assertTrue(listener2.called)
        listener3.assert_called_with(switch)
        listener4.assert_called_with(switch, True)

    @patch("pygame.PixelArray")
    def test_inactive_switch_event(self, *args):
        p.dmd.render = Mock()
        get_events = Mock()
        switch = p.switches["start_button"]
        get_events.return_value = [{
            "type": p.proc.SWITCH_OPENED,
            "value": switch.number
        }]
        p.proc.api.get_events = get_events

        listener2 = Mock()
        listener3 = Mock()
        listener4 = Mock()

        p.events.on("switch_start_button_inactive", listener2)
        p.events.on("switch_inactive", listener3)
        p.events.on("switch", listener4)

        pin.proc.process()
        p.events.dispatch()

        self.assertTrue(listener2.called)
        listener3.assert_called_with(switch)
        listener4.assert_called_with(switch, False)

    @patch("pygame.PixelArray")
    def test_active_opto_switch_event(self, *args):
        p.dmd.render = Mock()
        get_events = Mock()
        switch = p.switches["trough"]
        get_events.return_value = [{
            "type": p.proc.SWITCH_OPENED,
            "value": switch.number
        }]
        p.proc.api.get_events = get_events

        listener = Mock()
        p.events.on("switch_trough_active", listener)
        pin.proc.process()
        p.events.dispatch()
        self.assertTrue(listener.called)


    @patch("pygame.PixelArray")
    def test_inactive_opto_switch_event(self, *args):
        p.dmd.render = Mock()
        get_events = Mock()
        switch = p.switches["trough"]
        get_events.return_value = [{
            "type": p.proc.SWITCH_CLOSED,
            "value": switch.number
        }]
        p.proc.api.get_events = get_events

        listener = Mock()
        p.events.on("switch_trough_inactive", listener)
        pin.proc.process()
        p.events.dispatch()
        self.assertTrue(listener.called)

    @patch("pygame.PixelArray")
    @patch("pin.proc.log")
    def test_invalid_event(self, log, *args):
        p.dmd.render = Mock()
        get_events = Mock()
        get_events.return_value = [{
            "type": 10,
            "value": 0
        }]
        p.proc.api.get_events = get_events
        pin.proc.process()
        self.assertTrue(log.error.called)

    @patch("pygame.PixelArray")
    @patch("pin.proc.virtual_dmd")
    def test_process_virtual(self, *args):
        p.dmd.render = Mock()
        p.options["virtual"] = True
        pin.proc.process()


