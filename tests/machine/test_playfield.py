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

from pin.lib import p
from tests import fixtures

import logging
log = logging.getLogger("pin")

class TestPlayfield(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.playfield = p.modes["playfield"]
        self.playfield.enable(children=True)
        p.modes["simulator"].enable()

    def test_live(self):
        p.modes["trough"].eject()
        p.now = 1
        fixtures.loop()
        p.switches["ball_launch_button"].activate()
        p.now = 2
        fixtures.loop()
        p.now = 3
        fixtures.loop()
        p.now = 4
        fixtures.loop()
        self.assertTrue(self.playfield.live)


    def test_dead(self):
        p.modes["trough"].eject()
        p.now = 1
        fixtures.loop()
        p.switches["ball_launch_button"].activate()
        p.now = 2
        fixtures.loop()
        p.now = 3
        fixtures.loop()
        p.now = 4
        fixtures.loop()
        self.assertTrue(self.playfield.live)
        p.switches["trough_4"].activate()
        fixtures.loop()
        p.now = 5
        fixtures.loop()
        self.assertFalse(self.playfield.live)


