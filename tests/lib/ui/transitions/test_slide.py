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
from pin.lib.ui.transitions import SlideIn, SlideOut

import unittest
from mock import Mock
from tests import fixtures

class TestSlideIn(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_left(self):
        slide = SlideIn(direction="left")
        slide.frame = Mock(pygame.Surface)
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (dmd.width, 0))

        slide.frame.reset_mock()
        slide.progress = 0.5
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (dmd.width / 2, 0))

        slide.frame.reset_mock()
        slide.progress = 1.0
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (0, 0))

    def test_right(self):
        slide = SlideIn(direction="right")
        slide.frame = Mock(pygame.Surface)
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (-dmd.width, 0))

        slide.frame.reset_mock()
        slide.progress = 0.5
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (-dmd.width / 2, 0))

        slide.frame.reset_mock()
        slide.progress = 1.0
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (0, 0))

    def test_down(self):
        slide = SlideIn(direction="down")
        slide.frame = Mock(pygame.Surface)
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (0, -dmd.height))

        slide.frame.reset_mock()
        slide.progress = 0.5
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (0, -dmd.height / 2))

        slide.frame.reset_mock()
        slide.progress = 1.0
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (0, 0))

    def test_up(self):
        slide = SlideIn(direction="up")
        slide.frame = Mock(pygame.Surface)
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (0, dmd.height))

        slide.frame.reset_mock()
        slide.progress = 0.5
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (0, dmd.height / 2))

        slide.frame.reset_mock()
        slide.progress = 1.0
        slide.draw()
        slide.frame.blit.assert_called_with(slide.after, (0, 0))

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            SlideIn(direction="foo")

    def test_str(self):
        self.assertEquals("slide_in", str(SlideIn()))


class TestSlideOut(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_right(self):
        slide = SlideOut(direction="right")
        slide.frame = Mock(pygame.Surface)
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (0, 0))

        slide.frame.reset_mock()
        slide.progress = 0.5
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (dmd.width / 2, 0))

        slide.frame.reset_mock()
        slide.progress = 1.0
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (dmd.width, 0))

    def test_left(self):
        slide = SlideOut(direction="left")
        slide.frame = Mock(pygame.Surface)
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (0, 0))

        slide.frame.reset_mock()
        slide.progress = 0.5
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (-dmd.width / 2, 0))

        slide.frame.reset_mock()
        slide.progress = 1.0
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (-dmd.width, 0))

    def test_up(self):
        slide = SlideOut(direction="up")
        slide.frame = Mock(pygame.Surface)
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (0, 0))

        slide.frame.reset_mock()
        slide.progress = 0.5
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (0, -dmd.height / 2))

        slide.frame.reset_mock()
        slide.progress = 1.0
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (0, -dmd.height))

    def test_down(self):
        slide = SlideOut(direction="down")
        slide.frame = Mock(pygame.Surface)
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (0, 0))

        slide.frame.reset_mock()
        slide.progress = 0.5
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (0, dmd.height / 2))

        slide.frame.reset_mock()
        slide.progress = 1.0
        slide.draw()
        slide.frame.blit.assert_called_with(slide.before, (0, dmd.height))

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            SlideOut(direction="foo")

    def test_str(self):
        self.assertEquals("slide_out", str(SlideOut()))

