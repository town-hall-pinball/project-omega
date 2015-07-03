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

class Mode(Handler):

    def setup(self):
        self.display = ui.Panel(name="mm3_stage_select")
        self.text = ui.Text("MM3")
        self.display.add(self.text)

    def on_enable(self):
        p.dmd.add(self.display)


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

