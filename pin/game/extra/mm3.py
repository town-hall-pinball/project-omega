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

import os

import p
from pin import resources, ui, util
from pin.handler import Handler

available = os.path.exists(os.path.join(resources.base_dir, "extra", "mm3"))

bosses = [
    ( "mm3_spark_man",  "Spark Man" ),
    ( "mm3_snake_man",  "Snake Man" ),
    ( "mm3_needle_man", "Needle Man" ),
    ( "mm3_hard_man",   "Hard Man" ),
    ( "mm3_top_man",    "Top Man" ),
    ( "mm3_gemini_man", "Gemini Man" ),
    ( "mm3_magnet_man", "Magnet Man" ),
    ( "mm3_shadow_man", "Shadow Man" )
]

class StageSelectDisplay(Handler):

    def setup(self):
        self.display = ui.Panel(name="mm3_stage_select")
        self.selected = util.Cycle(bosses)
        self.boss = ui.Image(left=0)

        self.instructions = ui.Text("Flippers to Select", font="r7",
                padding_left=32, fill=None)
        self.push_start = ui.Text("PUSH START", padding_left=32, fill=None)

        ui.valign((self.instructions, self.push_start))
        self.display.add((self.boss, self.instructions, self.push_start))
        self.push_start.do(ui.effects.Pulse(self.push_start))
        self.update()

        self.on("switch_flipper_left", self.previous)
        self.on("switch_flipper_right", self.next)

    def previous(self):
        self.selected.previous()
        self.update()
        p.mixer.play("mm3_select")

    def next(self):
        self.selected.next()
        self.update()
        p.mixer.play("mm3_select")

    def update(self):
        self.boss.update(image=self.selected.get()[0])


class GameStartDisplay(Handler):

    def setup(self):
        self.selected = None
        self.display = ui.Panel(name="mm3_game_start")
        self.background = ui.Image("mm3_background")
        self.text_container = ui.Panel(
            left=0,
            height=14,
            fill=None,
        )
        self.image = ui.Image(
            left=10,
            padding=[0, 2],
            fill=0
        )
        self.name = ui.Text(
            fill=None,
            padding_left=10 + 38,
            padding_bottom=1,
            case="title"
        )
        self.display.add((
            self.background,
            self.text_container,
            self.image,
            self.name
        ))

    def on_enable(self):
        self.wait(1.75, self.tear_end)
        self.image.update(image=self.selected[0], enabled=True)

    def tear_end(self):
        self.wait(1.50, self.blend_out)
        self.wait(3.25, self.show_name)

    def blend_out(self):
        self.text_container.do(ui.effects.BlendOut(self.text_container))

    def show_name(self):
        name = self.selected[1]
        self.name.do(ui.effects.Typewriter(self.name, name))


class Mode(Handler):

    def setup(self):
        self.stage_select = StageSelectDisplay("mm3_stage_select")
        self.game_start = GameStartDisplay("mm3_game_start")

        self.handlers = [ self.stage_select, self.game_start ]
        self.on("switch_start_button", self.select)
        self.timer = None

    def on_enable(self):
        p.dmd.clear()
        p.mixer.play("mm3_stage_select")
        self.stage_select.enable(transition=ui.transitions.Tear())
        self.timer = self.wait(30, self.timeout)

    def select(self):
        if self.game_start.enabled:
            return
        self.stage_select.disable()
        self.game_start.selected = self.stage_select.selected.get()
        self.game_start.enable(transition=ui.transitions.Tear())
        p.mixer.play("mm3_game_start")
        self.cancel(self.timer)
        self.wait(8.0, self.finish)

    def timeout(self):
        self.disable()
        p.modes["attract"].enable()

    def finish(self):
        self.disable()
        p.modes["attract"].enable()
        p.mixer.play(self.stage_select.selected.get()[0])


def init():
    if not available:
        return False

def load():
    if not available:
        return False

    resources.load_images(
        ("mm3_background",      "extra/mm3/images/background.dmd"),
        ("mm3_gemini_man",      "extra/mm3/images/gemini_man.dmd"),
        ("mm3_hard_man",        "extra/mm3/images/hard_man.dmd"),
        ("mm3_magnet_man",      "extra/mm3/images/magnet_man.dmd"),
        ("mm3_needle_man",      "extra/mm3/images/needle_man.dmd"),
        ("mm3_shadow_man",      "extra/mm3/images/shadow_man.dmd"),
        ("mm3_snake_man",       "extra/mm3/images/snake_man.dmd"),
        ("mm3_spark_man",       "extra/mm3/images/spark_man.dmd"),
        ("mm3_top_man",         "extra/mm3/images/top_man.dmd"),
    )

    resources.register_music(
        ("mm3_game_start",      "extra/mm3/music/game_start.ogg"),
        ("mm3_gemini_man",      "extra/mm3/music/gemini_man.ogg"),
        ("mm3_hard_man",        "extra/mm3/music/hard_man.ogg"),
        ("mm3_magnet_man",      "extra/mm3/music/magnet_man.ogg"),
        ("mm3_needle_man",      "extra/mm3/music/needle_man.ogg"),
        ("mm3_shadow_man",      "extra/mm3/music/shadow_man.ogg"),
        ("mm3_snake_man",       "extra/mm3/music/snake_man.ogg"),
        ("mm3_spark_man",       "extra/mm3/music/spark_man.ogg"),
        ("mm3_stage_select",    "extra/mm3/music/stage_select.ogg"),
        ("mm3_top_man",         "extra/mm3/music/top_man.ogg")
    )

    resources.load_sounds(
        ("mm3_select",          "extra/mm3/sounds/select.ogg")
    )

