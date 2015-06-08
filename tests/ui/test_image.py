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

import p
from pin import util, ui

import unittest
from mock import Mock, patch
from tests import fixtures

class TestImage(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        image = Mock()
        image.get_width = Mock()
        image.get_width.return_value = 20
        image.get_height = Mock()
        image.get_height.return_value = 10
        p.images["test"] = image

    @patch("pin.dmd.create_frame")
    def test_auto_size(self, patch):
        image = ui.Image("test")
        image.revalidate()
        self.assertEquals(20, image.width)
        self.assertEquals(10, image.height)

    @patch("pin.dmd.create_frame")
    def test_auto_size_empty(self, patch):
        image = ui.Image()
        image.revalidate()
        self.assertEquals(0, image.width)
        self.assertEquals(0, image.height)



