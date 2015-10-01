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

import argparse
import logging
import logging.handlers
import os
import time

import pygame
from pin.lib import p, brand, util
from pin.lib.virtual import dmd as virtual_dmd, proc as virtual_proc

from pin.config import default, platform, startup
from pin import extra, machine

def parse_arguments():
    parser = argparse.ArgumentParser(prog=brand.prog)
    parser.add_argument("-c", "--console", action="store_true", default=False,
        help="also print log file to console")
    parser.add_argument("-d", "--develop", action="store_true", default=False,
        help="enable debugging options used for development")
    parser.add_argument("-f", "--fast", action="store_true", default=False,
        help="fast startup, immediately go to attract mode")
    parser.add_argument("--font",
        help="show the FONT in the browser")
    parser.add_argument("--image",
        help="show the IMAGE in the browser")
    parser.add_argument("-m", "--metrics", action="store_true", default=False,
        help="collect execution metrics and display at program end")
    parser.add_argument("--movie",
        help="show the MOVIE in the browser")
    parser.add_argument("--music",
        help="play the MUSIC in the browser")
    parser.add_argument("-s", "--simulate", action="store_true", default=False,
        help="Simulate the P-ROC")
    parser.add_argument("--sound",
        help="play the SOUND in the browser")
    parser.add_argument("-q", "--quiet", action="store_true", default=False,
        help="Do not emit any sounds")

    p.options = vars(parser.parse_args())
    if p.options["develop"]:
        p.options["console"] = True
    p.options["virtual"] = p.options["develop"]

def init_logging():
    log_file = os.path.join("var", "{}.log".format(brand.prog))
    log_format = "%(asctime)s %(name)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(log_format, date_format)
    file_handler = logging.handlers.WatchedFileHandler(log_file)
    file_handler.setFormatter(formatter)

    root = logging.getLogger("pin")
    root.setLevel(logging.INFO)
    root.addHandler(file_handler)

    if p.options["console"]:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)

    return root

def init():
    p.data.load(p.defaults)
    p.data.save()
    if p.options["virtual"]:
        virtual_dmd.init()
    if p.options["simulate"]:
        p.proc.api = virtual_proc
    else:
        from pinproc import PinPROC
        p.proc.api = PinPROC(p.platform.name)
    p.proc.init()

def bind():
    from pin.lib.data import data
    p.data = data

    from pin.config import default
    p.defaults = default.settings

    from pin.lib import dmd
    p.dmd = dmd

    from pin.lib import engine
    p.engine = engine

    from pin.lib import events
    p.events = events

    from pin.lib import resources
    p.fonts = resources.fonts
    p.images = resources.images
    p.movies = resources.movies
    p.music = resources.music
    p.sounds = resources.sounds

    from pin.lib import mixer
    p.mixer = mixer

    from pin.lib import proc
    p.proc = proc

    from pin.lib import timers
    p.timers = timers

    from pin.lib import keyboard
    p.keyboard = keyboard

def run():
    parse_arguments()
    log = init_logging()
    log.info("{}, Version {}".format(brand.name, brand.version))

    try:
        import debug
        debug.init()
    except ImportError as ie:
        pass

    pygame.init()
    p.platform = platform
    machine.init()
    bind()
    init()

    if p.options["develop"]:
        p.engine.processors += [p.keyboard.process]
    p.engine.processors += [p.proc.process]
    p.engine.processors += [p.timers.service]
    p.engine.processors += [p.events.dispatch]

    p.now = time.time()
    startup.init()
    extra.init()
    startup.bootstrap()
    p.engine.run()

def shutdown(exit_code):
    try:
        if p.events:
            p.events.trigger("shutdown")
    except Exception as e:
        logging.getLogger("pin").exception("error during shutdown")
    logging.getLogger("pin").info("exited with return code {}"
            .format(exit_code))
    os._exit(exit_code)

exit_code = 0
try:
    run()
    shutdown(0)
except KeyboardInterrupt as ki:
    logging.getLogger("pin").info("exiting on console interrupt")
    shutdown(0)
except Exception as e:
    logging.getLogger("pin").exception("exiting on unexpected error")
    exit_code = 1
    raise


