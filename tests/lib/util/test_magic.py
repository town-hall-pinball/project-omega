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

from pin.lib import p, util
import unittest
from mock import MagicMock as Mock
from tests import fixtures

class TestMagic(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.listener = Mock()
        self.magic = util.MagicSequence("test", [
            "flipper_left",
            "flipper_right",
            "flipper_left"
        ], self.listener)
        self.magic.enable()

    def test_trigger(self):
        p.events.post("switch", p.switches["flipper_left"], True)
        p.events.post("switch", p.switches["flipper_right"], True)
        p.events.post("switch", p.switches["flipper_left"], True)
        p.events.dispatch()
        self.assertTrue(self.listener.called)

    def test_abort(self):
        p.events.post("switch", p.switches["flipper_left"], True)
        p.events.post("switch", p.switches["flipper_right"], True)
        p.events.post("switch", p.switches["flipper_right"], True)
        p.events.post("switch", p.switches["flipper_left"], True)
        p.events.dispatch()
        self.assertFalse(self.listener.called)

    def test_restart(self):
        p.events.post("switch", p.switches["flipper_left"], True)
        p.events.post("switch", p.switches["flipper_right"], True)
        p.events.post("switch", p.switches["flipper_left"], True)
        p.events.post("switch", p.switches["flipper_left"], True)
        p.events.post("switch", p.switches["flipper_right"], True)
        p.events.post("switch", p.switches["flipper_left"], True)
        p.events.dispatch()
        self.assertEquals(2, self.listener.call_count)

    def test_ignore_inactive(self):
        p.events.post("switch", p.switches["flipper_left"], False)
        p.events.post("switch", p.switches["flipper_right"], False)
        p.events.post("switch", p.switches["flipper_left"], False)
        p.events.dispatch()
        self.assertFalse(self.listener.called)



