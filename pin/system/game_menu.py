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

from pin.lib import p, brand, ui, util
from pin.lib.ui import effects
from pin.lib.handler import Handler

game_list = [
    { "name": "Practice",       "mode": "practice" },
    { "name": "Classic",        "mode": "classic"  },
    { "name": brand.name,       "mode": "attract"  },
]

class Mode(Handler):

    def setup(self):
        self.display = ui.Panel(name="game_select")
        self.top = ui.Text("Flippers to Select Game", font="a5", color=0x8)
        self.game = ui.Text("Game")
        self.bottom = ui.Text("Press Start", font="a5", color=0x8)
        ui.valign((self.top, self.game, self.bottom))
        self.display.add((self.top, self.game, self.bottom))
        self.selected = util.Cycle(game_list)

        self.game.effect("blink", on=0.4, off=0.1, repeat=True)
        self.on("switch_flipper_left", self.previous)
        self.on("switch_flipper_right", self.next)
        self.on("switch_start_button", self.start_mode)
        self.update()

    def on_enable(self):
        p.dmd.clear()
        self.selected.index = 0
        self.update()
        p.mixer.play("game_select")

    def on_disable(self):
        p.mixer.stop()

    def previous(self):
        self.selected.previous()
        self.update()

    def next(self):
        self.selected.next()
        self.update()

    def update(self):
        self.game.show(self.selected.get()["name"].upper())

    def start_mode(self):
        mode = self.selected.get()["mode"]
        self.disable()
        p.modes[mode].enable()

