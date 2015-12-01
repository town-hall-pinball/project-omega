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

class TestMagnets(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.mode = p.modes["magnets"]

    def test_assist(self):
        self.mode.enable()
        self.assertTrue(p.coils["magnet_left"].auto)
        self.assertTrue(p.coils["magnet_center"].auto)
        self.assertTrue(p.coils["magnet_right"].auto)

        self.assertEquals("patter", p.coils["magnet_left"].auto["schedule"])
        self.assertEquals("patter", p.coils["magnet_center"].auto["schedule"])
        self.assertEquals("patter", p.coils["magnet_right"].auto["schedule"])

    def test_disable(self):
        self.mode.enable()
        self.mode.disable()
        self.assertFalse(p.coils["magnet_left"].auto)
        self.assertFalse(p.coils["magnet_center"].auto)
        self.assertFalse(p.coils["magnet_right"].auto)

