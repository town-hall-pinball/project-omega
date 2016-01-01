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

from pin.lib.data import data

import unittest
from mock import Mock, patch, mock_open
from tests import fixtures

class TestDevices(unittest.TestCase):

    def setUp(self):
        fixtures.reset()

    def test_load_override(self):
        contents = '{ "test": 12 }'
        with patch("__builtin__.open", mock_open(read_data=contents), create=True):
            data.load({"test": 34})
        self.assertEquals(12, data["test"])
        self.assertFalse(data["cleared"])

    def test_load_merge(self):
        contents = '{ "test": 12 }'
        with patch("__builtin__.open", mock_open(read_data=contents), create=True):
            data.load({"other": 34})
        self.assertEquals(12, data["test"])
        self.assertEquals(34, data["other"])

    @patch("__builtin__.open")
    def test_load_failure(self, mo):
        mo.side_effect = IOError
        contents = '{ "test": 12 }'
        data.load({})
        self.assertFalse("test" in data)
        self.assertTrue(data["cleared"])

    def test_save(self):
        data.read_only = False
        with patch("__builtin__.open", mock_open(), create=True) as mo:
            data["test"] = 12
            data.save()
        self.assertFalse(data.pop("save_failure", False))

    @patch("__builtin__.open")
    def test_save_failure(self, mo):
        data.read_only = False
        mo.side_effect = IOError
        data.save()
        self.assertTrue(data["save_failure"])





