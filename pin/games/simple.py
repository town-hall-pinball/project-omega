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

from pin.lib import p, score, ui
from pin.lib.game import Game

class Mode(Game):

    draining = False

    def game_setup(self):
        self.scoreboard = score.Classic(self)
        self.display = self.scoreboard.display
        self.on("drain", self.drain)
        self.on("home", self.home)
        self.on("switch_slingshot_left", self.slingshot)
        self.on("switch_slingshot_right", self.slingshot)

    def game_start(self):
        pass

    def game_add_player(self, player):
        player.update({
            "kickback": True
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

    def slingshot(self):
        self.score(10)


