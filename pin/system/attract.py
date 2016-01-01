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

from pin.lib import p, brand, score, ui, util
from pin.lib.ui.transitions import SlideIn, SlideOut
from pin.lib.handler import Handler

ON = 0x7f
__ = 0x00

lights = {
    "playfield_left":           [ON, __, __, __],
    "playfield_center":         [__, ON, __, ON],
    "playfield_right":          [__, __, ON, __],

    "circle_1":                 [__, __, ON, __, __, __],
    "circle_2":                 [__, ON, __, __, __, __],
    "circle_3":                 [ON, __, __, __, __, __],
    "circle_4":                 [__, __, __, __, __, ON],
    "circle_5":                 [__, __, __, __, ON, __],
    "circle_6":                 [__, __, __, ON, __, __],
    "circle_7":                 [__, __, ON, __, __, __],
    "circle_8":                 [__, ON, __, __, __, __],
    "circle_9":                 [ON, __, __, __, __, __],
    "circle_10":                [__, __, __, __, __, ON],
    "circle_11":                [__, __, __, __, ON, __],
    "circle_12":                [__, __, __, ON, __, __],
    "shoot_again":              [ON, __, __, ON, __, __],

    "outlane_left":             [ON, ON, __, __, __, __, __, __, __, __, __, __],
    "inlane_left":              [__, __, ON, ON, __, __, __, __, __, __, ON, ON],
    "inlane_right":             [__, __, __, __, ON, ON, __, __, ON, ON, __, __],
    "outlane_right":            [__, __, __, __, __, __, ON, ON, __, __, __, __],
    "kickback":                 [__, __, __, __, ON, ON, __, __, ON, ON, __, __],

    "orbit_left_sign":          [__, __, __, ON],
    "orbit_left_circle_3":      [ON, __, __, __],
    "orbit_left_arrow_2":       [__, ON, __, __],
    "orbit_left_arrow_1":       [__, __, ON, __],

    "orbit_right_arrow_2":      [ON, __],
    "orbit_right_arrow_1":      [__, ON],

    "ramp_left_sign_top":       [ON, __],
    "ramp_left_sign_bottom":    [__, ON],

    "ramp_left_circle_3":       [ON, __, __, __],
    "ramp_left_circle_2":       [__, ON, __, __],
    "ramp_left_circle_1":       [__, __, ON, __],
    "ramp_left_arrow":          [__, __, __, ON],

    "ramp_right_circle_3":      [ON, __, __, __],
    "ramp_right_circle_2":      [__, ON, __, __],
    "ramp_right_circle_1":      [__, __, ON, __],

    "ramp_right_arrow_2":       [ON, __],
    "ramp_right_arrow_1":       [__, ON],

    "saucer_arrow_2":           [ON, __],
    "saucer_arrow_1":           [__, ON],

    "scoop_center_arrow_4":     [ON, __, __, __],
    "scoop_center_arrow_3":     [__, ON, __, __],
    "scoop_center_arrow_2":     [__, __, ON, __],
    "scoop_center_arrow_1":     [__, __, __, ON],
    "scoop_center_circle":      [ON, __, ON, __],

    "scoop_left_arrow_3":       [ON, __, __, __],
    "scoop_left_arrow_2":       [__, ON, __, __],
    "scoop_left_arrow_1":       [__, __, ON, __],

    "standup_target_bottom":    [ON, __, __, __],
    "standup_target_top":       [__, __, ON, __],

    "toy_left":                 [__, ON, __, __],
    "toy_right":                [__, __, __, ON],

    "u_turn_left_circle_3":     [ON, __, __, __],
    "u_turn_left_circle_2":     [__, ON, __, __],
    "u_turn_left_circle_1":     [__, __, ON, __],
    "u_turn_left_arrow":        [__, __, __, ON],
    "u_turn_right_arrow":       [ON, __, ON, __],
}

mm3_sequence = [
    "flipper_left",
    "flipper_left",
    "flipper_left",
    "flipper_right",
    "flipper_right",
    "flipper_right",
    "ball_launch_button"
]

class Mode(Handler):

    thp = ui.Image("thp_logo")
    presents = ui.Text("PRESENTS")
    title = ui.Text(brand.name, font="t5exb")
    no_game = ui.Text("GAME OVER")
    anim = ui.Movie("x2")
    proc = ui.Image("p-roc")
    first = True

    def setup(self):
        credits = p.displays["credits"].display
        self.scoreboard = score.Classic(self)

        self.show = ui.Slides("attract.show", self, (
            #(score,                 3.0),
            (self.thp,                  3.0),
            (self.presents,             3.0, SlideIn(direction="left")),
            (self.title,                3.0),
            (self.no_game,              6.0),
            (credits,                   3.0),
            (self.scoreboard.display,   6.0),
            (self.anim,                 None),
            (self.proc,                 3.0)),
            repeat=True)
        self.on("switch_service_enter", self.start_service_mode)
        self.on("switch_flipper_left", self.show.next)
        self.on("switch_flipper_right", self.show.next)

        self.mm3 = util.MagicSequence("mm3.watcher", mm3_sequence,
                self.start_mm3)
        self.handlers += [self.mm3]
        self.light_show = util.LightShow("attract.light", 0.1, lights)

    def on_enable(self):
        if self.first:
            self.first = False
            p.mixer.play("introduction")
        self.show.start()
        self.mm3.enable()
        self.light_show.start()

    def on_disable(self):
        p.mixer.stop()
        self.show.stop()
        self.light_show.stop()

    def on_suspend(self):
        self.show.stop()

    def on_resume(self):
        self.show.start()

    def start_service_mode(self):
        p.modes["service"].enable()
        self.disable()
        p.mixer.play("service_enter")

    def start_mm3(self):
        if "mm3" in p.modes:
            self.disable()
            p.modes["mm3"].enable()

    def restart(self):
        self.show.index = 0
        self.enable()

    def game_over(self):
        p.mixer.play("introduction")
        self.show.index = 3
        self.enable()
        self.scoreboard.update()





