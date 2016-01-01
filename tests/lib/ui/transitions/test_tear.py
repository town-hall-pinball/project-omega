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

import pygame

from pin.lib import dmd
from pin.lib.ui.transitions import Tear

import unittest
from mock import Mock
from tests import fixtures

class TestTear(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.mid = dmd.height / 2

    def test_tear(self):
        tear = Tear()
        tear.frame = Mock(pygame.Surface)
        tear.draw()
        tear.frame.blit.assert_any_call(tear.after, (dmd.width, 0),
                area=(0, 0, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.after, (-dmd.width, self.mid),
                area=(0, self.mid, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.before, (0, 0),
                area=(0, 0, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.before, (0, self.mid),
                area=(0, self.mid, dmd.width, self.mid))

        tear.frame.reset_mock()
        tear.progress = 0.5
        tear.draw()
        tear.frame.blit.assert_any_call(tear.after, (dmd.width / 2, 0),
                area=(0, 0, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.after, (-dmd.width / 2, self.mid),
                area=(0, self.mid, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.before, (-dmd.width / 2, 0),
                area=(0, 0, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.before, (dmd.width / 2, self.mid),
                area=(0, self.mid, dmd.width, self.mid))

        tear.frame.reset_mock()
        tear.progress = 1.0
        tear.draw()
        tear.frame.blit.assert_any_call(tear.after, (0, 0),
                area=(0, 0, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.after, (0, self.mid),
                area=(0, self.mid, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.before, (-dmd.width, 0),
                area=(0, 0, dmd.width, self.mid))
        tear.frame.blit.assert_any_call(tear.before, (dmd.width, self.mid),
                area=(0, self.mid, dmd.width, self.mid))

    def test_tear_str(self):
        self.assertEquals("tear", str(Tear()))

