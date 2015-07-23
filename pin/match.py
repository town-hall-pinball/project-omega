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

log = logging.getLogger("pin.match")

class Player(dict):

    def __setitem__(self, key, value):
        super(Player, self).__setitem__(key, value)
        p.events.post("player_{}".format(key))


class Match(dict):

    def __init__(self):
        self.active = False
        self.live = False
        self.players = []
        self.player = 0
        self.ball = 1
        self.max_balls = 3
        self.max_players = 4

    def enable_playfield(self, enable=True):
        if enable:
            self.live = True
            p.devices.flippers.enable()
        else:
            self.live = False
            p.devices.flippers.disable()

    def disable_playfield(self):
        self.enable_playfield(False)

    def add_player(self):
        if self.active and self.ball > 1:
            log.warn("not adding player, past first ball")
            return
        if not self.active:
            self.players = []
            self.active = True
            p.events.post("start_match")
            self.enable_playfield()
        else:
            if len(self.players) == self.max_players:
              log.warn("not adding player, at maximum")
                return
            self.players += [Player()]
            p.events.post("add_player")

    def next_player(self):
        if self.player > len(self.players):
            if self.ball == self.max_balls:
                self.end_match()
                return
            self.ball += 1
            p.events.post("next_ball")
            self.player = 0
        else:
            self.player += 1
        p.events.post("next_player")

    def end_of_ball(self):
        self.disable_playfield()
        p.events.post("end_of_ball")

    def end_match(self):
        self.active = False
        p.events.post("end_match")

    def __setitem__(self, key, value):
        super(Match, self).__setitem__(key, value)
        p.events.post("match_{}".format(key))



