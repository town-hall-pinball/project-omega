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

from pin.lib import p, ui, util
from pin.lib.handler import Handler

class TiltWarningDisplay(ui.Notice):

    def __init__(self):
        super(TiltWarningDisplay, self).__init__(name="tilt_warning",
                duration=2.0, fill=0xf)
        self.message = ui.Text("WARNING", fill=0xf, color=0x0)
        self.add([self.message])
        self.message.effect("blink", duration=0.1, repeat=3)


class Mode(Handler):

    warnings = 0

    def setup(self):
        self.on("switch_tilt", self.check_tilt)
        self.on("switch_tilt_slam", self.slam_tilt)

    def on_enable(self):
        self.warnings = 0

    def check_tilt(self):
        self.warnings += 1
        if self.warnings > p.data["tilt_warnings"]:
            self.tilt()
        else:
            p.mixer.play("tilt_warning")
            p.dmd.interrupt(p.displays["tilt_warning"])

    def tilt(self):
        p.dmd.reset()
        p.dmd.add(p.displays["tilt"])
        p.events.post("tilt")

    def slam_tilt(self):
        p.dmd.reset()
        p.dmd.add(p.displays["slam_tilt"])
        p.events.post("slam_tilt")


def init():
    p.displays["tilt_warning"] = TiltWarningDisplay()
    p.displays["tilt"] = ui.message("TILT")
    p.displays["slam_tilt"] = ui.message("SLAM TILT")


