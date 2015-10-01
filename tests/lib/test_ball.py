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

from pin.lib import p, ball

import unittest
from mock import Mock
from tests import fixtures

class TestCaptures(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        for capture in ball.captures.values():
            capture.enable()

    def test_empty(self):
        self.assertEquals(0, ball.trough_count())

    def test_full_trough(self):
        p.switches["trough"].activate()
        p.switches["trough_2"].activate()
        p.switches["trough_3"].activate()
        p.switches["trough_4"].activate()
        fixtures.loop()
        self.assertEquals(4, ball.trough_count())
        self.assertTrue(ball.trough_ready())

    def test_staged_ball(self):
        p.switches["trough"].activate()
        p.switches["trough_2"].activate()
        p.switches["trough_3"].activate()
        p.switches["popper"].activate()
        fixtures.loop()
        self.assertEquals(4, ball.trough_count())

    def test_full_popper(self):
        p.switches["trough"].activate()
        p.switches["trough_2"].activate()
        p.switches["popper"].activate()
        p.switches["popper_2"].activate()
        fixtures.loop()
        self.assertEquals(3, ball.trough_count())
        self.assertFalse(ball.trough_ready())

    def test_trough_eject(self):
        trough = ball.captures["trough"]
        trough.eject()
        self.assertTrue(trough.ejecting)
        p.switches["shooter_lane"].activate()
        p.now = 1
        fixtures.loop()
        self.assertFalse(trough.ejecting)

    def test_trough_jam(self):
        trough = ball.captures["trough"]
        trough.eject()
        self.assertTrue(trough.ejecting)
        self.assertEquals(1, trough.eject_attempts)

        p.switches["trough_jam"].activate()
        p.now = 1
        fixtures.loop()
        self.assertTrue(trough.ejecting)
        self.assertEquals(2, trough.eject_attempts)

        p.now = 4
        fixtures.loop()
        self.assertTrue(trough.ejecting)
        self.assertEquals(3, trough.eject_attempts)

        p.now = 7
        p.switches["trough_jam"].deactivate()
        fixtures.loop()
        self.assertFalse(trough.ejecting)
        self.assertEquals(0, trough.eject_attempts)

    def test_give_up(self):
        trough = ball.captures["trough"]
        trough.eject()
        p.switches["trough_jam"].activate()
        p.now = 1
        for i in xrange(ball.max_eject_attempts - 1):
            p.now += 3
            fixtures.loop()
        self.assertTrue(trough.ejecting)
        p.now += 3
        fixtures.loop()
        self.assertFalse(trough.ejecting)
        self.assertTrue(trough.jammed)

    def test_popper(self):
        popper = ball.captures["popper"]
        popper.eject()
        p.now = 0.5
        p.switches["return_right"].activate()
        p.switches["return_right"].deactivate()
        fixtures.loop()
        self.assertFalse(popper.ejecting)

    def test_popper_jam(self):
        popper = ball.captures["popper"]
        popper.eject()
        fixtures.loop()
        self.assertTrue(popper.ejecting)
        self.assertEquals(1, popper.eject_attempts)
        p.now = 1
        fixtures.loop()
        self.assertTrue(popper.ejecting)
        self.assertEquals(2, popper.eject_attempts)


class TestSearch(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        ball.search_sequence = [
            p.coils["saucer"],
            p.coils["popper"]
        ]

    def test_search(self):
        listener1 = Mock()
        listener2 = Mock()
        p.events.on("coil_saucer", listener1)
        p.events.on("coil_popper", listener2)
        ball.search()
        fixtures.loop()
        self.assertTrue(listener1.called)
        p.now += ball.search_interval
        fixtures.loop()
        self.assertTrue(listener2.called)
        self.assertFalse(ball.search.running)

    def test_search_already_running(self):
        listener1 = Mock()
        listener2 = Mock()
        p.events.on("coil_saucer", listener1)
        p.events.on("coil_popper", listener2)
        ball.search()
        fixtures.loop()
        ball.search()
        self.assertTrue(listener1.called)
        self.assertFalse(listener2.called)
        self.assertTrue(ball.search.running)





