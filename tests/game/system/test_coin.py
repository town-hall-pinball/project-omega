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

import unittest
from tests import fixtures

class TestCoinDrop(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.coin = p.modes["coin"]
        self.coin.enable()

        p.data["coin_left"]     = 0.25
        p.data["coin_center"]   = 0.50
        p.data["coin_right"]    = 0.75
        p.data["coin_fourth"]   = 1.00

        p.data["pricing"] = 1.00

    def test_coin_left(self):
        p.events.post("switch_coin_left")
        p.events.dispatch()
        self.assertEquals(0.25, p.data["credits"])

    def test_coin_center(self):
        p.events.post("switch_coin_center")
        p.events.dispatch()
        self.assertEquals(0.50, p.data["credits"])

    def test_coin_right(self):
        p.events.post("switch_coin_right")
        p.events.dispatch()
        self.assertEquals(0.75, p.data["credits"])

    def test_coin_fourth(self):
        p.events.post("switch_coin_fourth")
        p.events.dispatch()
        self.assertEquals(1.00, p.data["credits"])


class TestCoin(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.coin = p.modes["coin"]
        self.coin.enable()
        p.data["coin_left"] = 0.25
        p.data["pricing"] = 0.50

    def test_paid_credit(self):
        p.events.post("switch_coin_left")
        p.events.dispatch()
        self.assertEquals(0.5, p.data["credits"])
        self.assertEquals(0.5, p.data["paid_credits"])
        self.assertEquals(0.25, p.data["earnings"])

        p.events.post("switch_coin_left")
        p.events.dispatch()
        self.assertEquals(1, p.data["credits"])
        self.assertEquals(1, p.data["paid_credits"])
        self.assertEquals(0.5, p.data["earnings"])

    def test_service_credit(self):
        p.events.post("switch_service_exit")
        p.events.dispatch()
        self.assertEquals(1, p.data["credits"])
        self.assertEquals(1, p.data["service_credits"])
        self.assertEquals(0, p.data["earnings"])





