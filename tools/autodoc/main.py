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

import os
from pin import config
from pin.config import platform
from pin.lib import p, devices

base_dir = os.path.dirname(__file__)
doc_dir = os.path.join(base_dir, "..", "..", "doc", "machine")

class Table(object):

    rows = None
    widths = None

    def __init__(self):
        self.rows = []

    def add(self, *row):
        if not self.widths:
            self.widths = [0] * len(row)
        for i, col in enumerate(row):
            self.widths[i] = max(self.widths[i], len(str(col)))
        self.rows += [row]

    def hr(self):
        strs = []
        for width in self.widths:
            strs += ["=" * width]
        return "  ".join(strs)

    def render(self):
        lines = []
        index = 0
        for row in self.rows:
            if index == 0:
                lines += [self.hr()]
            strs = []
            for i, col in enumerate(row):
                strs += [str(col).ljust(self.widths[i])]
            lines += ["  ".join(strs)]
            if index == 0:
                lines += [self.hr()]
            index += 1
        lines += [self.hr()]
        return "\n".join(lines)


def by_name(filename, title, objects):

    with open(os.path.join(doc_dir, filename + "_by_name.rst"), "w") as rst:
        rst.write(".. Generated by tools/autodoc.py\n")
        rst.write("\n")
        rst.write("================\n")
        rst.write(title + " by Name\n")
        rst.write("================\n")
        rst.write("\n")
        table = Table()
        table.add("Device", "Name", "Number", "Tags", "Original")
        for key in sorted(objects):
            o = objects[key]
            table.add(o.device, key, o.number,
                    ",".join(sorted(o.tags)), o.original)
        rst.write(table.render())
        rst.write("\n")

def by_device(filename, title, objects):
    with open(os.path.join(doc_dir, filename + "_by_device.rst"), "w") as rst:
        rst.write(".. Generated by tools/autodoc.py\n")
        rst.write("\n")
        rst.write("==================\n")
        rst.write(title + " by Device\n")
        rst.write("==================\n")
        rst.write("\n")
        table = Table()
        table.add("Device", "Name", "Number", "Tags", "Original")
        for o in sorted(objects.values(), key=lambda o: o.device):
            table.add(o.device, o.name, o.number,
                    ",".join(sorted(o.tags)), o.original)
        rst.write(table.render())
        rst.write("\n")



def run():
    p.platform = platform
    config.init()
    by_name("switches", "Switches", devices.switches)
    by_device("switches", "Switches", devices.switches)
    by_name("lamps", "Lamps", devices.lamps)
    by_device("lamps", "Lamps", devices.lamps)
    by_name("coils", "Coils", devices.coils)
    by_device("coils", "Coils", devices.coils)
    by_name("flashers", "Flashers", devices.flashers)
    by_device("flashers", "Flashers", devices.flashers)

