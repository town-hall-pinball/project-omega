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

import importlib
import logging
import time

coils = None
"""
Something :py:class:`pin.devices.Coil`
"""

data = None
"""
A :py:class:`pin.data <pin.data.Data>` object that contains all persistant
information tracked by the pinball machine.

Example to clear the current credit count::

    p.data["credits"] = 0
    p.data.save()
"""

defaults = None
dmd = None
displays = {}
effects = {}
events = None
fonts = None
game = None
gi = None
images = None
lamps = None
machine = None
modes = None
movies = None
mixer = None
music = None
now = time.time()
options = {}
proc = None
platform = None
namespace = None
save = None
switches = None
sounds = None
timers = None

def load_modes(names):
    global modes
    if modes is None:
        modes = {}
    for name in names:
        fullname = namespace + "." + name
        basename = name.split(".")[-1]
        try:
            m = importlib.import_module(fullname)
            create_mode = True
            if hasattr(m, "init"):
                create_mode = m.init() != False
            if create_mode:
                modes[basename] = m.Mode(basename + ".mode")
        except Exception as e:
            logging.getLogger("pin").error("Unable to load {}".format(fullname))
            raise


