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

from pin.lib import p

class Eject(object):

    ejecting = False
    retry_timer = None
    attempts = 0
    failed = False

    def __init__(self, handler, coil, retry_time=3.0, max_attempts=10):
        self.handler = handler
        self.coil = coil
        self.retry_time = retry_time
        self.max_attempts = max_attempts

    def reset(self):
        self.ejecting = False
        self.retry_attempts = 0
        self.failed = False
        self.handler.cancel(self.retry_timer)

    def eject(self):
        self.ejecting = True
        self.retry_attempts = 0
        self.failed = False
        self.handler.cancel(self.retry_timer)
        p.events.post("{}_ejecting".format(self.coil.name))
        self.pulse()

    def pulse(self):
        self.coil.pulse()
        self.attempts += 1
        self.retry_timer = self.handler.wait(self.retry_time, self.retry)

    def retry(self):
        if self.ejecting:
            if self.attempts < self.max_attempts:
                p.events.post("{}_retry".format(self.coil.name))
                self.pulse()
            else:
                self.failed = True
                p.events.post("{}_failed".format(self.coil.name))

    def success(self):
        self.ejecting = False
        self.handler.cancel(self.retry_timer)
        p.events.post("{}_ejected".format(self.coil.name))





