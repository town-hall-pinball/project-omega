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

from pin.lib import p
from pin.lib.handler import Handler

class Mode(Handler):

    def setup(self):
        self.on("loop_flipper_disable", self.adjust_lamp)

    def on_enable(self):
        p.coils["magnet_left"].auto_patter(
                p.switches["magnet_left"], 1, 1, notify=True)
        p.coils["magnet_center"].auto_patter(
                p.switches["magnet_center"], 1, 1, notify=True)
        p.coils["magnet_right"].auto_patter(
                p.switches["magnet_right"], 1, 1, notify=True)

        p.lamps["ramp_left_sign_bottom"].enable()

    def on_disable(self):
        p.coils["magnet_left"].auto_cancel()
        p.coils["magnet_center"].auto_cancel()
        p.coils["magnet_right"].auto_cancel()
        p.lamps["ramp_left_sign_bottom"].disable()

    def adjust_lamp(self):
        p.lamps["ramp_left_sign_bottom"].enable()

