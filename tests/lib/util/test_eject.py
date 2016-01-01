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

from pin.lib import p
from pin.lib.util import Eject

import unittest
from tests import fixtures
from mock import Mock

class TestEject(unittest.TestCase):

    def setUp(self):
        fixtures.reset()
        self.saucer = Eject(p.modes["saucer"], p.coils["saucer"])
        p.modes["saucer"].enable()

    def test_retry(self):
        success = Mock()
        retry = Mock()
        p.events.on("saucer_retry", retry)
        p.events.on("saucer_ejected", success)
        self.saucer.eject()
        p.now = 4
        fixtures.loop()
        self.assertFalse(success.called)
        self.assertTrue(retry.called)

    def test_success(self):
        success = Mock()
        retry = Mock()
        p.events.on("saucer_retry", retry)
        p.events.on("saucer_ejected", success)
        self.saucer.eject()
        fixtures.loop()
        self.saucer.success()
        fixtures.loop()
        p.now = 4
        fixtures.loop()
        self.assertTrue(success.called)
        self.assertFalse(retry.called)

    def test_failure(self):
        failed = Mock()
        p.events.on("saucer_failed", failed)
        self.saucer.max_attempts = 2
        self.saucer.eject()
        fixtures.loop()
        self.assertEquals(1, self.saucer.attempts)
        self.assertFalse(failed.called)
        p.now = 3
        fixtures.loop()
        self.assertEquals(2, self.saucer.attempts)
        self.assertFalse(failed.called)
        p.now = 6
        fixtures.loop()
        self.assertEquals(2, self.saucer.attempts)
        self.assertTrue(failed.called)



