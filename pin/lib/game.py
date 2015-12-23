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

import logging
from . import p, util
from .handler import Handler

log = logging.getLogger("pin.game")

class Player(dict):

    def __setitem__(self, key, value):
        super(Data, self).__setitem__(key, value)
        p.events.post("player_{}".format(key))


def create_player(index):
    player = Player({
        "index": index,
        "number": index + 1,
        "score": 0
    })
    return player


class Base(Handler):

    tilted = False

    def setup(self):
        self.handlers = [
            p.modes["playfield"],
            p.modes["plunger"],
        ]
        self.on("live", self.live_ball)
        self.on("tilt", self.tilt)
        self.on("slam_tilt", self.tilt)
        self.game_setup()

    def game_setup(self):
        pass

    def on_enable(self):
        if p.game:
            raise ValueError("Game ({}) already running".format(p.game.name))
        p.game = self
        self.tilted = False
        p.events.post("game_start")
        self.game_start()

    def game_start(self):
        pass

    def on_disable(self):
        p.game = None
        self.game_end()

    def game_end(self):
        pass

    def tilt(self):
        p.modes["playfield"].dead()
        self.tilted = True
        p.mixer.stop()
        self.game_tilt()

    def game_tilt(self):
        pass

    def live_ball(self):
        p.modes["plunger"].auto = True
        self.game_live_ball()

    def game_live_ball(self):
        pass



class Game(Base):

    name = None
    active = False
    players = []
    order = None
    ball = 0
    max_players = 4
    live = False

    def setup(self):
        super(Game, self).setup()
        self.on("new_player", self.new_player_check)

    def on_enable(self):
        self.players = []
        self.order = util.Cycle()
        self.active = True
        self.ball = 1
        p.players = self.players
        super(Game, self).on_enable()

    def new_player_check(self):
        if self.ball == 1 and len(self.players) < self.max_players:
            self.add_player()

    def add_player(self):
        index = len(self.players)
        if index >= self.max_players:
            raise ValueError("Too many players")
        player = create_player(index)
        self.players += [player]
        self.order.items += [player]
        p.events.post("add_player", player)
        p.notify("game", "Add Player {}".format(player["number"]))
        if not p.data["free_play"]:
            p.data["credits"] = p.data["credits"] - 1
            p.data.save()
        self.game_add_player(player)
        if player["number"] == 1:
            p.player = player
            p.events.post("next_player")
            self.game_next_player()

    def game_add_player(self):
        pass

    def next_player(self):
        p.player = self.order.next()
        if p.player["index"] == 0:
            self.ball += 1
            if self.ball > self.data("balls"):
                self.over()
        if self.active:
            p.events.trigger("next_player")
            p.notify("game", "Next Player")
            if p.player["index"] == 0:
                p.events.post("next_ball")
            p.notify("game", "Ball {}, Player {}".format(
                    self.ball, p.player["number"]))
            self.game_next_player()

    def game_next_player(self):
        pass

    def end_of_turn(self):
        p.events.post("end_of_turn")

    def over(self):
        self.active = False
        self.ball = 0
        p.events.trigger("game_over")
        p.notify("game", "Game Over")
        self.game_over()

    def data(self, name):
        return p.data[self.name + "." + name]




