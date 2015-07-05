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
import p
import pin
from pin import server
from pin.game import extra
from pin.virtual import dmd as virtual_dmd, proc as virtual_proc

def parse_arguments():
    parser = argparse.ArgumentParser(prog=pin.brand.prog)
    parser.add_argument("-c", "--console", action="store_true", default=False,
        help="also print log file to console")
    parser.add_argument("-d", "--develop", action="store_true", default=False,
        help="enable debugging options used for development")
    parser.add_argument("-f", "--fast", action="store_true", default=False,
        help="fast startup, immediately go to attract mode")
    parser.add_argument("-m", "--metrics", action="store_true", default=False,
        help="collect execution metrics and display at program end")
    parser.add_argument("-s", "--simulate", action="store_true", default=False,
        help="Simulate the P-ROC")
    parser.add_argument("-q", "--quiet", action="store_true", default=False,
        help="Do not emit any sounds")

    p.options = vars(parser.parse_args())
    if p.options["develop"]:
        p.options["console"] = True
    p.options["virtual"] = p.options["develop"]

def init_logging():
    log_file = os.path.join("var", "{}.log".format(pin.brand.prog))
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
    p.data = pin.data
    p.defaults = pin.game.config.defaults.defaults
    p.dmd = pin.dmd
    p.engine = pin.engine
    p.events = pin.events
    p.fonts = pin.resources.fonts
    p.images = pin.resources.images
    p.mixer = pin.mixer
    p.movies = pin.resources.movies
    p.music = pin.resources.music
    p.sounds = pin.resources.sounds
    p.proc = pin.proc
    p.timers = pin.timers

def run():
    parse_arguments()
    log = init_logging()
    log.info("{}, Version {}".format(pin.brand.name, pin.brand.version))

    try:
        import debug
        debug.init()
    except ImportError as ie:
        pass

    pygame.init()
    p.platform = pin.platform
    pin.machine.init()
    bind()
    init()

    if p.options["develop"]:
        p.engine.processors += [pin.keyboard.process]
    p.engine.processors += [pin.proc.process]
    p.engine.processors += [pin.timers.service]
    p.engine.processors += [pin.events.dispatch]

    p.now = time.time()
    pin.game.init()
    extra.init()
    pin.game.start()
    server.update()
    p.engine.run()

def shutdown(exit_code):
    try:
        server.stop()
    except Exception as e:
        logging.getLogger("pin").exception("Error during shutdown")
    logging.getLogger("pin").info("Exited with return code: {}"
            .format(exit_code))
    os._exit(exit_code)

exit_code = 0
try:
    run()
except KeyboardInterrupt as ki:
    logging.getLogger("pin").info("Exiting on console interrupt")
except Exception as e:
    logging.getLogger("pin").exception("Exiting on unexpected error")
    exit_code = 1
finally:
    shutdown(exit_code)

