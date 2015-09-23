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
Dictionary of :py:class:`pin.devices.Coil` objects keyed by identifier.

Example to fire the auto plunger coil::

    p.coils["auto_plunger"].pulse()

Coils are configured at :py:mod:`pin.machine.coils`
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
"""
Dictonary of defaults to be used if the persistant state in ``var/data.json``
is not available. Configured in :py:mod:`pin.game.config.defaults`
"""

dmd = None
displays = {}
effects = {}

events = None
"""
:py:mod:`The global event queue <pin.events>`

Example to register a function, `foo`, to be called when the left flipper
button is pressed::

    p.events.on("switch_left_flipper", foo)

"""

fonts = None
flashers = None
flippers = None
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
"""
The time at the start of the execution loop. Use this instead of
``time.time()`` for getting a consistant time value throughout the execution
loop.
"""

options = {}
"""
A dictionary of options passed on the command line.

Example to see if the ``-q`` or ``--quiet`` option was passed in::

    if p.options["quiet"]:
        print "quiet"
"""

proc = None
platform = None
namespace = None
save = None
service_menu = None
sounds = None
switches = None

timers = None
"""
:py:mod:`The global timer manager <pin.timers>`

Example to register a function, `foo`, to be called after two seconds have
elapsed::

    p.timers.wait(2.0, foo)

"""

def load_modes(names):
    global modes
    if modes is None:
        modes = {}
    for name in names:
        fullname = "pin." + name
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


def notify(mtype, message):
    logging.getLogger("pin.notice").debug(message)
    events.post("notice", mtype, message)


