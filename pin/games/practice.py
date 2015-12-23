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

from pin.lib import p, ui
from pin.lib.game import Base

class Mode(Base):

    expired = False
    magnets = True

    def game_setup(self):
        self.max_time = 0
        self.display = ui.Panel()
        self.time = ui.Text("0:00", font="bm10w")
        self.display.add((self.time,))
        self.ticker = None
        self.start_time = None

        self.on("enter_saucer", self.saucer)
        self.on("entering_popper", self.popper)
        self.on("drain", self.drain)
        self.on("home", self.home_check)
        self.on("switch_subway_left", self.subway_left)
        self.on("switch_drop_target", self.drop_target)

    def game_start(self):
        self.max_time = p.data["practice_timer"]
        self.expired = False
        self.magnets = True
        self.start_time = None
        self.update_time()
        self.enable_playfield()
        p.modes["trough"].eject()
        p.modes["drop_target"].down()
        p.mixer.play("credits")

    def game_end(self):
        p.timers.cancel(self.ticker)

    def enable_playfield(self):
        p.modes["playfield"].enable(children=True)
        p.modes["kickback"].enable()
        p.modes["magnets"].enable()
        p.modes["flippers"].enable_loop()

    def update_time(self):
        elapsed = 0
        if self.start_time:
            elapsed = p.now - self.start_time
        remaining = self.max_time - elapsed
        if remaining < 0:
            remaining = 0
            p.modes["playfield"].dead()
            self.expired = True
            p.timers.cancel(self.ticker)
            p.mixer.stop()
        minutes = int(remaining / 60)
        seconds = int(remaining % 60)
        self.time.show("{}:{:02d}".format(minutes, seconds))

    def game_live_ball(self):
        if not self.start_time:
            self.ticker = p.timers.tick(self.update_time)
            self.start_time = p.now

    def saucer(self):
        if self.magnets:
            self.magnets = False
            ui.notify("MAGNETS DISABLED", duration=2.0)
            p.modes["magnets"].disable()
        else:
            self.magnets = True
            ui.notify("MAGNETS ENABLED", duration=2.0)
            p.modes["magnets"].enable()
        self.wait(2.0, self.eject_saucer)

    def eject_saucer(self):
        p.modes["saucer"].eject()

    def popper(self):
        p.modes["playfield"].popper_eject(entering=True)

    def subway_left(self):
        p.modes["drop_target"].up()

    def drop_target(self):
        p.modes["drop_target"].down()

    def drain(self):
        p.modes["playfield"].ball_status()
        if not self.tilted and not self.expired:
            p.modes["trough"].eject()

    def game_tilt(self):
        p.timers.cancel(self.ticker)

    def home_check(self):
        if self.tilted or self.expired:
            self.game_over()

    def game_over(self):
        p.mixer.play("introduction")
        ui.notify("GAME OVER", duration=5.0, callback=self.done)

    def done(self):
        self.disable()
        p.modes["attract"].restart()



