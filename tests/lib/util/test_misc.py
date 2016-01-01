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

from pin.lib import util
import unittest

class TestToList(unittest.TestCase):

    def test_to_list(self):
        self.assertEquals([1], util.to_list(1))

    def test_already_list(self):
        self.assertEquals([1], util.to_list([1]))


class TestDictMerge(unittest.TestCase):

    def test_simple(self):
        a = { "x": 1 }
        b = { "y": 2 }
        expected = { "x": 1, "y": 2 }
        self.assertEquals(expected, util.dict_merge(a, b))

    def test_deep(self):
        a = { "x": { "one": 1 } }
        b = { "x": { "two": 2 } }
        expected = { "x": { "one": 1, "two": 2 } }
        self.assertEquals(expected, util.dict_merge(a, b))

    def test_many(self):
        a = { "x": { "one": 1 } }
        b = { "x": { "two": 2 } }
        c = { "x": { "three": 3 } }
        expected = { "x": { "one": 1, "two": 2, "three": 3 } }
        self.assertEquals(expected, util.dict_merge(a, b, c))

    def test_non_dict(self):
        self.assertEquals("foo", util.dict_merge({}, "foo"))


class TestFraction(unittest.TestCase):

    def test_fraction_0(self):
        self.assertEquals("0", util.fraction(0))

    def test_fraction_025(self):
        self.assertEquals("1/4", util.fraction(0.25))

    def test_fraction_1_3(self):
        self.assertEquals("1/3", util.fraction(1.0/3.0))

    def test_fraction_050(self):
        self.assertEquals("1/2", util.fraction(0.5))

    def test_fraction_075(self):
        self.assertEquals("3/4", util.fraction(0.75))

    def test_fraction_575(self):
        self.assertEquals("5 3/4", util.fraction(5.75))

    def test_fraction_200(self):
        self.assertEquals("2", util.fraction(2.0))

