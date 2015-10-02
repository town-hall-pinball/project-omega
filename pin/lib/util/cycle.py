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

__all__ = ["Cycle"]

class Cycle():

    index = 0
    items = None

    def __init__(self, items=None):
        if not items:
            items = []
        self.items = list(items)

    def get(self):
        return self.items[self.index]

    def next(self):
        self.index += 1
        if self.index >= len(self.items):
            self.index = 0
        return self.get()

    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.items) - 1
        return self.get()

    def select(self, value):
        for i, other in enumerate(self.items):
            if value == other:
                self.index = i
                return
        raise ValueError("Item not found: {}".format(value))

