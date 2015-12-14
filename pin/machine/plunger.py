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

from pin.lib import p
from pin.lib.handler import Handler

class Mode(Handler):

    auto = False

    def setup(self):
        self.on("switch_shooter_lane_active", self.shooter_lane_active)
        self.on("switch_shooter_lane_inactive", self.shooter_lane_inactive)
        self.on("switch_ball_launch_button", self.ball_launch_button)
        self.on_switch("shooter_lane", self.auto_launch_check, 0.25)

    def on_enable(self):
        self.auto = False

    def on_disable(self):
        p.lamps["ball_launch_button"].disable()

    def shooter_lane_active(self):
        p.lamps["ball_launch_button"].patter()

    def shooter_lane_inactive(self):
        p.lamps["ball_launch_button"].disable()

    def ball_launch_button(self):
        if p.switches["shooter_lane"].active:
            self.eject()

    def auto_launch_check(self):
        if self.auto:
            self.eject()

    def eject(self):
        p.notify("game", "Launch")
        p.coils["auto_plunger"].pulse()
        p.events.post("launch")

