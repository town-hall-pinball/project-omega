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

from pin.lib import p, ui, util

class Classic(object):

    initial = True

    def __init__(self, handler):
        self.handler = handler

        self.display = ui.Panel()
        self.player = ui.Text(top=4)
        self.players = [
            ui.Text(left=0, top=0),
            ui.Text(right=0, top=0, x_align="right"),
            ui.Text(left=0, bottom=7),
            ui.Text(right=0, bottom=7, x_align="right")
        ]
        self.ball = ui.Text(bottom=0, left=0, width=54, font="bm3", x_align="right")
        self.credits_right = ui.Text(bottom=0, left=64, font="bm3")
        self.credits_center = ui.Text(bottom=0, font="bm3")

        self.display.add((self.player, self.players[0], self.players[1],
                self.players[2], self.players[3], self.ball,
                self.credits_right, self.credits_center))

        self.handler.on("data_credits", self.update)
        self.handler.on("add_player", self.update)
        self.handler.on("next_player", self.next_player)
        self.handler.on("player_score", self.score)
        self.update()

    def next_player(self):
        self.initial = True
        self.update()

    def score(self):
        self.initial = False
        self.update()

    def update(self, *args, **kwargs):
        self.update_score(self.player, 0, single=True)
        for index, player in enumerate(self.players):
            self.update_score(player, index, single=False)

        if p.game:
            self.ball.show("BALL {}".format(p.game.ball))
            self.credits_right.show(util.credits_string())
            self.credits_center.hide()
        else:
            self.ball.hide()
            self.credits_right.hide()
            self.credits_center.show(util.credits_string())

    def update_score(self, text, index, single):
        show = True
        if single and len(p.players) > 1:
            show = False
        if not single and len(p.players) == 1:
            show = False
        if index >= len(p.players):
            show = False
        if show:
            score = p.players[index]["score"]
            self.update_score_size(text, single, index)
            text.show(util.format_score(score))
            if index == p.player["index"] and self.initial and p.game:
                text.effect("blink", duration=0.15, repeat=True)
            elif index == p.player["index"] and p.game:
                text.effect("laser")
            else:
                text.effect_cancel()
        else:
            text.hide()

    # Adapted from
    # https://github.com/preble/pyprocgame/blob/master/procgame/modes/scoredisplay.py#L104
    def update_score_size(self, text, single, index):
        score = p.players[index]["score"]
        if single:
            if score < 1e9:
                text.update(font="bm10w")
            elif score < 1e10:
                text.update(font="bm10")
            else:
                text.update(font="bm10n")
        elif not single and p.game and p.player["index"] == index:
            if score < 1e6:
                text.update(font="bm8w")
            elif score < 1e7:
                text.update(font="bm8")
            else:
                text.update(font="bm8n")
        else:
            if score < 1e6:
                text.update(font="bm5w")
            elif score < 1e7:
                text.update(font="bm5")
            else:
                text.update(font="bm5n")

