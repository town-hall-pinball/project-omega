# Copyright (c) 2014 - 2016 townhallpinball.org
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

from pin.lib import p, devices
from pin.lib.handler import Handler

class Mode(Handler):

    left = None
    right = None
    upper = None

    def setup(self):
        self.left = p.flippers["left"]
        self.right = p.flippers["right"]
        self.upper = p.flippers["right_up"]
        self.on("mode_magnets_enable", self.magnets_enable)

    def on_enable(self):
        self.left.auto_pulse()
        self.right.auto_pulse()

    def on_disable(self):
        self.left.auto_cancel()
        self.right.auto_cancel()
        self.upper.auto_cancel()
        p.lamps["ramp_left_sign_bottom"].disable()

    def enable_loop(self):
        self.upper.auto_pulse()
        p.lamps["ramp_left_sign_bottom"].patter()
        p.notify("mode", "loop flipper enabled")
        p.events.post("loop_flipper_enable")

    def disable_loop(self):
        self.upper.auto_cancel()
        p.lamps["ramp_left_sign_bottom"].disable()
        p.notify("mode-disabled", "loop flipper disabled")
        p.events.post("loop_flipper_disable")

    def magnets_enable(self):
        if self.upper.auto:
            p.lamps["ramp_left_sign_bottom"].patter()


def init():
    devices.add_flippers({
        "left": {
            "label": "Flipper, Left",
            "device": "flipper_lower_left_main",
            "hold_device": "flipper_lower_left_hold",
            "switch": "flipper_left"
        },
        "right": {
            "label": "Flipper, Right",
            "device": "flipper_lower_right_main",
            "hold_device": "flipper_lower_right_hold",
            "switch": "flipper_right"
        },
        "right_up": {
            "label": "Flipper, Right Upper",
            "device": "flipper_upper_right_main",
            "hold_device": "flipper_upper_right_hold",
            "switch": "flipper_right_up"
        }
    })
