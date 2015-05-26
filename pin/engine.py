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
import pin

__all__ = [
    "processors", "fps", "exit", "loops", "run_time", "sleep_time",
    "overruns", "run"
]

processors = []
"""
Functions invoked on each run loop.
"""

fps = 35
"""
Number of loops per second that the engine should execute. If a loop
completes early, the engine sleeps for the remaining time. If a loop
completes late, the engine starts the next loop immediately.
"""

exit = False
"""
If `True`, the engine will exit after the current loop completes.
"""

loops = 0
"""
Number of loops exceuted. This value is only updated when starting the
program with the ``--metrics`` option.
"""

run_time = 0
"""
Average time, in milliseconds, spent in the run loop. This value is only
updated when starting the program with the ``--metrics`` option.
"""

sleep_time = 0
"""
Average time, in milliseconds, spent sleeping after executing the run loop.
This value is only updated when starting the program with the ``--metrics``
option.
"""

overruns = 0
"""
Total number of times the run loop was late.
"""

log = logging.getLogger("pin.engine")

def reset():
    """
    Clears the processor run list and resets all metrics.
    """
    global processors, exit, loops, run_time, overruns, sleep_time
    processors = []
    exit = False
    loops = 0
    run_time = 0
    overruns = 0
    sleep_time = 0

def run():
    """
    Executes the run loop until `exit` is `True` or an exception is raised.
    """
    try:
        pin.events.post("reset")
        while not exit:
            frame()
    except KeyboardInterrupt as ki:
        pass
    finally:
        metrics = pin.options.get("metrics", False)
        if metrics and loops > 0:
            run = (run_time / loops) * 1000
            sleep = (sleep_time / loops) * 1000
            late = (float(overruns) / loops) * 100
            log.info("run: {:.2f}ms, sleep: {:.0f}ms, late: {:.1f}%"
                    .format(run, sleep, late))

def frame():
    start = time.time()
    pin.now = start
    max_time = 1.0 / fps
    for processor in processors:
        processor()
    elapsed = time.time() - start
    remaining = max_time - elapsed

    metrics = pin.options.get("metrics", False)
    if metrics:
        global loops, run_time, overruns, sleep_time
        loops += 1
        run_time += elapsed
        if elapsed > max_time:
            overruns += 1
        if remaining > 0:
            sleep_time += remaining

    if remaining > 0:
        time.sleep(remaining)




