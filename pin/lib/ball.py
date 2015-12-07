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

import collections
import logging

from . import p, util
from .handler import Handler

log = logging.getLogger("pin.ball")

search_sequence = []
search_interval = 0.25

class Search(object):

    running = False
    index = 0
    timer = None

    def __call__(self):
        if self.running:
            log.warn("search already running")
            return
        log.debug("searching")
        p.notify("game", "Ball Search")
        self.running = True
        self.next()

    def next(self):
        search_sequence[self.index].pulse()
        self.index += 1
        if self.index == len(search_sequence):
            self.index = 0
            self.running = False
        else:
            self.timer = p.timers.wait(search_interval, self.next)


search = Search()





