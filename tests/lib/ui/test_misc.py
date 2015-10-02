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

from pin.lib import util, ui
import unittest

class TestValign(unittest.TestCase):

    def test_single(self):
        c = ui.Component(height=12)
        ui.valign([c])
        self.assertEquals(10, c.style["top"])

    def test_multiple(self):
        c1 = ui.Component(height=12)
        c2 = ui.Component(height=10)
        ui.valign([c1, c2], padding=0)
        self.assertEquals(5, c1.style["top"])
        self.assertEquals(17, c2.style["top"])

    def test_padding(self):
        c1 = ui.Component(height=12)
        c2 = ui.Component(height=10)
        ui.valign([c1, c2], padding=2)
        self.assertEquals(4, c1.style["top"])
        self.assertEquals(18, c2.style["top"])
