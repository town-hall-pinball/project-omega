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

class TestSimulator(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        p.data["simulator_enabled"] = True
        self.sim = p.modes["simulator"]
        fixtures.loop()

    def test_initial(self):
        self.assertTrue(p.switches["trough"].active)
        self.assertTrue(p.switches["trough_2"].active)
        self.assertTrue(p.switches["trough_3"].active)
        self.assertTrue(p.switches["popper"].active)

    def test_stop(self):
        p.data["simulator_enabled"] = False
        fixtures.loop()
        self.assertFalse(p.switches["trough"].active)
        self.assertFalse(p.switches["trough_2"].active)
        self.assertFalse(p.switches["trough_3"].active)
        self.assertFalse(p.switches["popper"].active)

    def test_trough_feed(self):
        p.coils["trough"].pulse()
        fixtures.loop()

        self.assertTrue(p.switches["trough"].active)
        self.assertTrue(p.switches["trough_2"].active)
        self.assertFalse(p.switches["trough_3"].active)
        self.assertTrue(p.switches["popper"].active)
        self.assertTrue(p.switches["shooter_lane"].active)
        self.assertEquals(0, self.sim.free)

    def test_launch(self):
        p.coils["trough"].pulse()
        p.coils["auto_plunger"].pulse()
        fixtures.loop()

        self.assertTrue(p.switches["trough"].active)
        self.assertTrue(p.switches["trough_2"].active)
        self.assertFalse(p.switches["trough_3"].active)
        self.assertTrue(p.switches["popper"].active)
        self.assertFalse(p.switches["shooter_lane"].active)
        self.assertEquals(1, self.sim.free)

    def test_drain(self):
        p.coils["trough"].pulse()
        p.coils["auto_plunger"].pulse()
        p.switches["trough_4"].activate()
        fixtures.loop()

        self.assertTrue(p.switches["trough"].active)
        self.assertTrue(p.switches["trough_2"].active)
        self.assertTrue(p.switches["trough_3"].active)
        self.assertFalse(p.switches["trough_4"].active)
        self.assertTrue(p.switches["popper"].active)
        self.assertFalse(p.switches["shooter_lane"].active)
        self.assertEquals(0, self.sim.free)

    def test_disable(self):
        switch = p.switches["drop_target"]
        switch.activate()
        fixtures.loop()
        self.assertTrue(switch.active)
        p.coils["drop_target_up"].pulse()
        fixtures.loop()
        self.assertFalse(switch.active)

    def test_no_free_balls(self):
        p.switches["trough_4"].activate()
        fixtures.loop()
        p.switches["trough_4"].deactivate()
        fixtures.loop()
        self.assertTrue(p.switches["trough_3"].active)
        self.assertFalse(p.switches["trough_4"].active)
        self.assertEquals(0, self.sim.free)

    def test_ball_not_at_source(self):
        p.coils["popper"].pulse()
        fixtures.loop()
        self.assertEquals(1, self.sim.free)
        p.coils["popper"].pulse()
        self.assertEquals(1, self.sim.free)


