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
import pin
from pin.virtual import dmd as virtual_dmd, proc as virtual_proc

def config():
    from pin.platforms import wpc
    from pin.machines import no_fear

    pin.platform = wpc
    pin.machine = no_fear


def parse_arguments():
    parser = argparse.ArgumentParser(prog=pin.brand.PROG)
    parser.add_argument("-c", "--console", action="store_true", default=False,
        help="also print log file to console")
    parser.add_argument("-d", "--develop", action="store_true", default=False,
        help="enable debugging options used for development")
    parser.add_argument("-m", "--metrics", action="store_true", default=False,
        help="collect execution metrics and display at program end")
    parser.add_argument("-s", "--simulate", action="store_true", default=False,
        help="Simulate the P-ROC")

    pin.options = vars(parser.parse_args())
    if pin.options["develop"]:
        pin.options["console"] = True
        pin.options["virtual"] = True

def init_logging():
    log_file = os.path.join("var", "{}.log".format(pin.brand.PROG))
    log_format = "%(asctime)s %(name)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(log_format, date_format)
    file_handler = logging.handlers.WatchedFileHandler(log_file)
    file_handler.setFormatter(formatter)

    root = logging.getLogger("pin")
    root.setLevel(logging.INFO)
    root.addHandler(file_handler)

    if pin.options["console"]:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)

    return root


def init_proc():
    if pin.options["simulate"]:
        pin.proc.api = virtual_proc
    else:
        from pinproc import PinPROC
        pin.proc.api = PinPROC(p.platform["name"])
    pin.proc.api.reset(1)


def init():
    parse_arguments()
    log = init_logging()
    log.info("{}, Version {}".format(pin.brand.NAME, pin.brand.VERSION))
    config()
    pin.machine.init()
    if pin.options["virtual"]:
        virtual_dmd.init()
    init_proc()


def run():
    init()
    pin.modes.init()
    if pin.options["develop"]:
        pin.engine.processors += [pin.keyboard.process]
    pin.engine.processors += [pin.proc.process]
    pin.engine.processors += [pin.timers.process]
    pin.engine.processors += [pin.events.process]
    pin.engine.run()

run()
