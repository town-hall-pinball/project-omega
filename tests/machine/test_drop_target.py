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

import unittest
from mock import Mock

from pin.lib import p
from tests import fixtures

class TestDropTarget(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.mode = p.modes["drop_target"]
        self.mode.enable()

    def test_down(self):
        listener = Mock()
        p.events.on("coil_drop_target_down", listener)
        self.mode.down()
        fixtures.loop()
        self.assertTrue(listener.called)

    def test_already_down(self):
        listener = Mock()
        p.events.on("coil_drop_target_down", listener)
        p.switches["drop_target"].activate()
        fixtures.loop()
        p.now = 100
        self.mode.down()
        fixtures.loop()
        self.assertFalse(listener.called)

    def test_down_on_hit(self):
        listener = Mock()
        p.events.on("coil_drop_target_down", listener)
        p.switches["drop_target"].activate()
        self.mode.down()
        fixtures.loop()
        self.assertTrue(listener.called)

    def test_up(self):
        listener = Mock()
        p.events.on("coil_drop_target_up", listener)
        p.switches["drop_target"].activate()
        fixtures.loop()
        self.mode.up()
        fixtures.loop()
        self.assertTrue(listener.called)

    def test_already_up(self):
        listener = Mock()
        p.events.on("coil_drop_target_up", listener)
        p.now = 100
        self.mode.up()
        fixtures.loop()
        self.assertFalse(listener.called)



