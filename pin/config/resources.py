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

from pin.lib import resources

def load():
    resources.load_images(
        ("p-roc",                   "images/p-roc.dmd"),

        ("info",                    "images/notice/info.png"),
        ("warning",                 "images/notice/warning.png"),

        ("service_animations",      "images/service/animations.dmd"),
        ("service_audits",          "images/service/audits.dmd"),
        ("service_browse",          "images/service/browse.dmd"),
        ("service_clear",           "images/service/clear.dmd"),
        ("service_coils",           "images/service/coils.dmd"),
        ("service_debug",           "images/service/debug.dmd"),
        ("service_flashers",        "images/service/flashers.dmd"),
        ("service_flippers",        "images/service/flippers.png"),
        ("service_font",            "images/service/font.dmd"),
        ("service_game_settings",   "images/service/game_settings.dmd"),
        ("service_image",           "images/service/image.png"),
        ("service_lamps",           "images/service/lamps.dmd"),
        ("service_money",           "images/service/money.dmd"),
        ("service_more",            "images/service/more.png"),
        ("service_music",           "images/service/music.dmd"),
        ("service_server",          "images/service/server.dmd"),
        ("service_settings",        "images/service/settings.dmd"),
        ("service_sounds",          "images/service/sounds.dmd"),
        ("service_switches",        "images/service/switches.dmd"),
        ("service_tests",           "images/service/tests.dmd"),
        ("service_utilities",       "images/service/utilities.dmd"),
        ("thp_logo",                "images/thp_logo.dmd"),
    )
    resources.register_movies(
        ("x2",                      "movies/X2_from_left_ship_from_right - 90-Android.mpg"),
        ("tina_test",               "movies/tinatest.dmd")
    )
    resources.load_sounds(
        ("boot",                "sounds/boot.ogg"),
        ("tilt_warning",        "sounds/tilt_warning.ogg"),
        ("settings_cleared",    "sounds/settings_cleared.ogg"),
        ("service_cancel",      "sounds/service/cancel.ogg"),
        ("service_enter",       "sounds/service/enter.ogg"),
        ("service_exit",        "sounds/service/exit.ogg"),
        ("service_save",        "sounds/service/save.ogg"),
        ("service_select",      "sounds/service/select.ogg"),
        ("service_switch_edge", "sounds/service/switch_edge.ogg"),
        ("coin_drop",           "sounds/coinDrop.ogg"),
        ("warning",             "sounds/warning.ogg")
    )
    resources.register_music(
        ("credits",         "music/Credits.ogg",       { "start_time": 2.25, "loop": True}),
        ("introduction",    "music/Introduction.ogg",  { "start_time": 0.50 }),
        ("game_select",     "music/game_select.ogg",   { "loop": True }),
        ("pinball_wizard",  "music/pinball_wizard.ogg",{ "start_time": 1.00 }),
    )
    resources.load_fonts(
        ("t5exb",   "fonts/pf_tempesta_five_extended_bold.ttf", 8),
        ("t5ex",    "fonts/pf_tempesta_five_extended.ttf", 8),
        ("t5cdb",   "fonts/pf_tempesta_five_condensed_bold.ttf", 8),
        ("t5cd",    "fonts/pf_tempesta_five_condensed.ttf", 8),
        ("t5cpb",   "fonts/pf_tempesta_five_compressed_bold.ttf", 8),
        ("t5cp",    "fonts/pf_tempesta_five_compressed.ttf", 8),
        ("t5b",     "fonts/pf_tempesta_five_bold.ttf", 8),
        ("t5",      "fonts/pf_tempesta_five.ttf", 8),
        ("r7b",     "fonts/pf_ronda_seven_bold.ttf", 8),
        ("r7",      "fonts/pf_ronda_seven.ttf", 8),
        ("a5",      "fonts/pf_arma_five.ttf", 8),
        ("c128",    "fonts/PetMe128.ttf", 8),
        ("c128_16", "fonts/PetMe128.ttf", 16),

        ("bm3",     "fonts/bitmap/bm3.dmd"),
        ("bm3n",    "fonts/bitmap/bm3n.dmd"),
        ("bm3w",    "fonts/bitmap/bm3w.dmd"),
        ("bm5",     "fonts/bitmap/bm5.dmd"),
        ("bm5n",    "fonts/bitmap/bm5n.dmd"),
        ("bm5w",    "fonts/bitmap/bm5w.dmd"),
        ("bm6",     "fonts/bitmap/bm6.dmd"),
        ("bm8",     "fonts/bitmap/bm8.dmd"),
        ("bm8n",    "fonts/bitmap/bm8n.dmd"),
        ("bm8w",    "fonts/bitmap/bm8w.dmd"),
        ("bm10",    "fonts/bitmap/bm10.dmd"),
        ("bm10n",   "fonts/bitmap/bm10n.dmd"),
        ("bm10w",   "fonts/bitmap/bm10w.dmd"),
        ("bmsf",    "fonts/bitmap/bmsf.dmd"),

    )
    resources.alias_fonts(
        ("r7b",     "title")
    )
