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
    "saucer_little_points":         2500,
    "saucer_big_points":          100000,
    "loop_base":                  200000,
    "loop_each":                   12500,
}

class Mode(Game):

    draining = False
    looping = False

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
        self.on("loop", self.loop)
        self.on("loop_exit", self.loop_exit)

    def game_start(self):
        pass

    def game_add_player(self, player):
        player.update({
            "kickback": True,
            "saucers": 0,
            "saucer_big_points": False,
            "drop_target_locked": False,
            "loop_enabled": False,
            "loops": 0,
        })

    def game_next_player(self):
        self.draining = False
        p.modes["playfield"].enable(children=True)
        p.modes["magnets"].enable()
        p.modes["trough"].eject()
        p.modes["drop_target"].down()
        p.mixer.play("credits")
        p.lamps["scoop_left_arrow_1"].patter()

        if p.player["kickback"]:
            p.modes["kickback"].enable()
        if p.player["loop_enabled"]:
            self.enable_loop()

    def slingshot(self):
        self.score(scores["slingshot"])

    def popper(self):
        p.modes["playfield"].popper_eject(entering=True)

    def subway_left(self):
        self.score(scores["subway_left"])
        self.drop_target_lock()
        self.enable_saucer_big_points()
        self.enable_loop()

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
            score = scores["saucer_big_points"]
            fscore = util.format_score(score)
            ui.notify(("SAUCER", fscore), duration=2.0)
            self.score(score)
            p.player["saucers"] += 1
            self.disable_saucer_big_points()
        else:
            self.score(scores["saucer_little_points"])
        self.wait(2.0, p.modes["saucer"].eject)

    def enable_loop(self):
        p.player["loop_enabled"] = True
        p.modes["flippers"].enable_loop()

    def disable_loop(self):
        p.player["loop_enabled"] = False
        p.modes["flippers"].disable_loop()

    def loop(self):
        self.looping = True
        score = scores["loop_base"] + (scores["loop_each"] * p.player["loops"])
        fscore = util.format_score(score)
        ui.notify(("LOOP", fscore), duration=2.0)
        p.player["loops"] += 1

    def loop_exit(self):
        if self.looping:
            self.looping = False
            self.disable_loop()
            self.drop_target_unlock()

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



