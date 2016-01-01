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

import logging
from ..handler import Handler

log = logging.getLogger("pin.magic")

class MagicSequence(Handler):

    def __init__(self, name, switches, callback):
        self.switches = switches
        self.callback = callback
        self.index = 0
        super(MagicSequence, self).__init__(name)

    def setup(self):
        self.on("switch", self.check)

    def check(self, switch, active):
        if not active:
            return
        if switch.name != self.switches[self.index]:
            if self.index != 0:
                log.debug("rejected")
            self.index = 0
            return
        log.debug("accepted")
        self.index += 1
        if self.index == len(self.switches):
            log.debug("triggered")
            self.callback()
            self.index = 0

