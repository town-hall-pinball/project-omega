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

import time
import logging

import p

class Engine(object):

    handlers = None
    exit = False
    loops = 0
    run_time = 0
    sleep_time = 0
    overruns = 0
    fps = 35

    def __init__(self, handlers=None):
        self.log = logging.getLogger("pin.engine")
        self.handlers = handlers or []

    def run(self):
        try:
            p.events.post("reset")
            while not self.exit:
                self.loop()
        except KeyboardInterrupt as ki:
            pass
        finally:
            if p.options["metrics"] and self.loops > 0:
                run = (self.run_time / self.loops) * 1000
                sleep = (self.sleep_time / self.loops) * 1000
                overruns = (float(self.overruns) / self.loops) * 100
                self.log.info("run: {:.2f}ms, sleep: {:.0f}ms, late: {:.1f}%"
                        .format(run, sleep, overruns))

    def loop(self):
        start = time.time()
        max_time = 1.0 / self.fps
        for handler in self.handlers:
            handler.handle()
        elapsed = time.time() - start
        remaining = max_time - elapsed
        p.events.dispatch()

        if p.options["metrics"]:
            self.loops += 1
            self.run_time += elapsed
            if elapsed > max_time:
                self.overruns += 1
            if remaining > 0:
                self.sleep_time += remaining

        if remaining > 0:
            time.sleep(remaining)


class PROC(object):

    DMD_READY = 5

    def __init__(self):
        pass

    def handle(self):
        events = p.proc.get_events()
        for event in events:
            if event["type"] == self.DMD_READY:
                frame = p.dmd.render()
                if p.dmd_virtual:
                    p.dmd_virtual.update(frame)


