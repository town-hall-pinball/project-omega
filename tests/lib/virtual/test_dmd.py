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
from pin.lib.virtual import dmd

import unittest
from mock import Mock, patch

def create_surface():
    return pygame.Surface((128, 32))

class TestDMD(unittest.TestCase):

    def setUp(self):
        self.surface = create_surface()

    # Coverage only
    @patch("pygame.display.get_surface")
    @patch("pygame.display.update")
    @patch("pygame.display.set_mode")
    def test_init(self, mock_get_surface, *args):
        mock_get_surface.return_value = self.surface
        dmd.init()

    # Coverage only
    @patch("pygame.display.get_surface")
    @patch("pygame.display.update")
    @patch("pygame.display.set_mode")
    def test_invalidate(self, mock_get_surface, *args):
        mock_get_surface.return_value = self.surface
        dmd.invalidate()

    @patch("pygame.display.get_surface")
    @patch("pygame.display.update")
    @patch("pygame.display.set_mode")
    def test_update(self, mock_get_surface, *args):
        mock_get_surface.return_value = self.surface
        frame1 = create_surface()
        # Make sure there is an actual dot that needs to be rendered.
        frame1.set_at((0, 0), 1)
        dmd.update(frame1)


