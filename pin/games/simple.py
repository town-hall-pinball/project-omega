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

from pin.lib import p, score, ui, util
from pin.lib.game import Game

scores = {
    "slingshot":                      10,
    "subway_left":                  1000,
    "saucer_little_points":        10000,
    "saucer_big_points":          100000,
}

class Mode(Game):

    draining = False

    def game_setup(self):
        self.scoreboard = score.Classic(self)
        self.display = self.scoreboard.display
        self.on("drain", self.drain)
        self.on("home", self.home)
        self.on("switch_slingshot_left", self.slingshot)
        self.on("switch_slingshot_right", self.slingshot)
        self.on("switch_subway_left", self.subway_left)
        self.on("enter_saucer", self.saucer)
        self.on("entering_popper", self.popper)
        self.on("drop_target", self.drop_target_hit)

    def game_start(self):
        pass

    def game_add_player(self, player):
        player.update({
            "kickback": True,
            "saucers": 0,
            "saucer_big_points": False,
            "drop_target_locked": False,
        })

    def game_next_player(self):
        self.draining = False
        p.modes["playfield"].enable(children=True)
        if p.player["kickback"]:
            p.modes["kickback"].enable()
        p.modes["magnets"].enable()
        p.modes["trough"].eject()
        p.modes["drop_target"].down()
        p.mixer.play("credits")
        p.lamps["scoop_left_arrow_1"].patter()

    def slingshot(self):
        self.score(scores["slingshot"])

    def popper(self):
        p.modes["playfield"].popper_eject(entering=True)

    def subway_left(self):
        self.score(scores["subway_left"])
        self.drop_target_lock()
        self.enable_saucer_big_points()

    def drop_target_lock(self):
        p.player["drop_target_locked"] = True
        p.modes["drop_target"].up()
        p.lamps["scoop_left_arrow_1"].disable()

    def drop_target_unlock(self):
        p.player["drop_target_locked"] = False
        p.lamps["scoop_left_arrow_1"].enable()

    def drop_target_hit(self):
        if not p.player["drop_target_locked"]:
            p.modes["drop_target"].down()
            p.lamps["scoop_left_arrow_1"].patter()

    def enable_saucer_big_points(self):
        p.player["saucer_big_points"] = True
        p.lamps["saucer_arrow_1"].patter()

    def disable_saucer_big_points(self):
        p.player["saucer_big_points"] = False
        p.lamps["saucer_arrow_1"].disable()

    def saucer(self):
        if p.player["saucer_big_points"]:
            score = util.format_score(scores["saucer_big_points"])
            ui.notify(("SAUCER", score), duration=2.0)
            self.score(scores["saucer_big_points"])
            self.disable_saucer_big_points()
        else:
            self.score(scores["saucer_little_points"])
        self.wait(2.0, p.modes["saucer"].eject)

    def drain(self):
        self.draining = True
        p.modes["plunger"].auto = False
        p.mixer.stop()

    def home(self):
        if self.draining:
            self.next_player()

    def game_over(self):
        self.disable()
        p.modes["attract"].game_over()



