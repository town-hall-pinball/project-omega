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
import p
from pin import util

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


class Game(object):

    name = None
    active = False
    players = []
    order = None
    ball = 0
    max_players = 4

    def __init__(self, name="main"):
        self.name = name

    def start(self):
        if self.active:
            raise ValueError("Game ({}) already started".format(self.name))
        self.players = []
        self.order = util.Cycle()
        self.active = True
        self.ball = 1
        p.events.post("game_start", self.name)
        p.events.post("game_start_" + self.name)
        self.add_player()
        p.players = self.players
        p.player = self.players[0]
        p.events.post("next_player")

    def add_player(self):
        if self.ball == 1 and len(self.players) < self.max_players:
            index = len(self.players)
            player = create_player(index)
            self.players += [player]
            self.order.items += [player]
            p.events.post("add_player", player)
            p.notify("game", "Add Player {}".format(player["number"]))
        else:
            raise ValueError("Cannot add player")

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

    def end_of_turn(self):
        p.events.post("end_of_turn")

    def over(self):
        self.active = False
        self.ball = 0
        p.events.trigger("game_over")
        p.notify("game", "Game Over")

    def data(self, name):
        return p.data[self.name + "." + name]



