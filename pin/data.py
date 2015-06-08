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

import json
import logging
import os
from . import util

__all__ = ["data"]

log = logging.getLogger("pin.data")
path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        "..", "var", "data.json"))

class Data(dict):

    def load(self, defaults):
        log.debug("Loading data from {}".format(path))
        util.dict_merge(self, defaults)
        try:
            with open(path) as fp:
                saved = json.load(fp)
                saved["cleared"] = False
                util.dict_merge(self, saved)
        except Exception as ie:
            log.error("Unable to load data file: {}".format(ie))

    def save(self):
        log.debug("Saving data to {}".format(path))
        try:
            with open(path, "w") as fp:
                json.dump(self, fp)
        except Exception as ie:
            log.error("Unable to save data file: {}".format(ie))

    def reset(self, defaults):
        log.debug("Resetting data to defaults")
        self.clear()
        util.dict_merge(self, defaults)


data = Data()

