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

import pygame

from pin.lib import p
from pin.lib.ui.transitions import Transition

import unittest
from tests import fixtures

class TestTransition(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_progress(self):
        trans = Transition("name", duration=10)
        trans.render(None, None, None)
        self.assertEquals(0, trans.progress)

        p.now = 5
        trans.render(None, None, None)
        self.assertEquals(0.5, trans.progress)

        p.now = 15
        trans.render(None, None, None)
        self.assertEquals(1, trans.progress)

    def test_reset(self):
        trans = Transition("name", duration=10)
        p.now = 15
        trans.render(None, None, None)
        trans.reset()
        self.assertEquals(0, trans.progress)

