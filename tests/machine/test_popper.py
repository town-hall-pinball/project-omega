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

from pin.lib import p

import unittest
from tests import fixtures
from mock import Mock

class TestPopper(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.popper = p.modes["popper"]
        self.popper.enable()

    def test_entering_via_left(self):
        entering = Mock()
        p.events.on("entering_popper", entering)
        p.switches["subway_left"].activate()
        fixtures.loop()
        self.assertEquals(1, entering.call_count)
        p.switches["subway_center"].activate()
        fixtures.loop()
        self.assertEquals(1, entering.call_count)

    def test_entering_via_center(self):
        entering = Mock()
        p.events.on("entering_popper", entering)
        p.switches["subway_center"].activate()
        fixtures.loop()
        self.assertEquals(1, entering.call_count)

    def test_enter(self):
        enter = Mock()
        p.events.on("enter_popper", enter)
        p.switches["popper_2"].activate()
        fixtures.loop()
        self.assertTrue(enter.called)

    def test_eject_and_exit(self):
        exit = Mock()
        p.events.on("exit_popper", exit)
        self.popper.eject()
        fixtures.loop()
        p.now = 1
        fixtures.loop()
        p.switches["return_right"].activate()
        fixtures.loop()
        self.assertTrue(exit.called)

    def test_count_change(self):
        p.switches["popper"].activate()
        fixtures.loop()
        p.now = 1
        fixtures.loop()
        self.assertEquals(1, self.popper.balls)
        p.switches["popper_2"].activate()
        fixtures.loop()
        p.now = 2
        fixtures.loop()
        self.assertEquals(2, self.popper.balls)

    def test_disable(self): # Coverage only
        self.popper.disable()



