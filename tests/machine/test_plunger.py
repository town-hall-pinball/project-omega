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

import unittest
from mock import patch

from pin.lib import p
from tests import fixtures

class TestPlunger(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.mode = p.modes["plunger"]
        self.mode.enable()

    def test_initial(self):
        self.assertFalse(self.mode.auto)

    def test_shooter_lane_active(self):
        p.switches["shooter_lane"].activate()
        fixtures.loop()
        self.assertEquals("patter",
                p.lamps["ball_launch_button"].state["schedule"])

    def test_shooter_lane_inactive(self):
        p.switches["shooter_lane"].activate()
        fixtures.loop()
        p.switches["shooter_lane"].deactivate()
        fixtures.loop()
        self.assertEquals("disable",
                p.lamps["ball_launch_button"].state["schedule"])

    def test_manual_launch(self):
        with patch.object(p.coils["auto_plunger"], "pulse") as launch:
            p.switches["shooter_lane"].activate()
            p.switches["ball_launch_button"].activate()
            fixtures.loop()
            self.assertTrue(launch.called)

    def test_manual_launch_not_ready(self):
        with patch.object(self.mode, "launch") as launch:
            p.switches["ball_launch_button"].activate()
            fixtures.loop()
            self.assertFalse(launch.called)

    def test_auto_launch(self):
        with patch.object(self.mode, "launch") as launch:
            self.mode.auto = True
            p.switches["shooter_lane"].activate()
            fixtures.loop()
            p.now = 1
            fixtures.loop()
            self.assertTrue(launch.called)

    def test_no_auto_launch(self):
        with patch.object(self.mode, "launch") as launch:
            p.switches["shooter_lane"].activate()
            fixtures.loop()
            p.now = 1
            fixtures.loop()
            self.assertFalse(launch.called)

    def test_disable(self):
        p.lamps["ball_launch_button"].disable()
        self.mode.disable()
        self.assertEquals("disable",
                p.lamps["ball_launch_button"].state["schedule"])


