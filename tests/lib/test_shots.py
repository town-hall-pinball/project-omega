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

from pin.lib import p, shots
import unittest
from tests import fixtures
from mock import Mock

class TestShots(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_left_orbit(self):
        listen_left = Mock()
        listen_right = Mock()
        p.events.on("shot_orbit_left", listen_left)
        p.events.on("shot_orbit_right", listen_right)

        p.events.post("playfield_enable")
        p.switches["orbit_left"].activate()
        p.switches["orbit_right"].activate()
        fixtures.loop()

        self.assertTrue(listen_left.called)
        self.assertFalse(listen_right.called)

    def test_right_orbit(self):
        listen_left = Mock()
        listen_right = Mock()
        p.events.on("shot_orbit_left", listen_left)
        p.events.on("shot_orbit_right", listen_right)

        p.events.post("playfield_enable")
        p.switches["orbit_right"].activate()
        p.switches["orbit_left"].activate()
        fixtures.loop()

        self.assertFalse(listen_left.called)
        self.assertTrue(listen_right.called)

    def test_playfield_disable(self):
        listen_left = Mock()
        listen_right = Mock()
        p.events.on("shot_orbit_left", listen_left)
        p.events.on("shot_orbit_right", listen_right)

        p.events.post("playfield_enable")
        p.events.post("playfield_disable")
        p.switches["orbit_right"].activate()
        p.switches["orbit_left"].activate()
        fixtures.loop()

        self.assertFalse(listen_left.called)
        self.assertFalse(listen_right.called)

    def test_drain(self):
        listener = Mock()
        p.events.on("drain", listener)
        p.proc.switch_active(p.switches["trough_4"])
        p.events.dispatch()
        self.assertTrue(listener.called)

    def test_user_switch(self):
        listen = Mock()
        p.events.on("drain", listen)

        p.events.post("playfield_enable")
        p.switches["service_enter"].activate()
        fixtures.loop()
        self.assertFalse(listen.called)
