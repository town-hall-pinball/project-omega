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

from pin import resources

def load():
    resources.load_images(
        ("thp_logo",                "images/thp_logo.dmd"),
        ("service_animations",      "images/service/animations.dmd"),
        ("service_audits",          "images/service/audits.dmd"),
        ("service_browse",          "images/service/browse.dmd"),
        ("service_clear",           "images/service/clear.dmd"),
        ("service_coils",           "images/service/coils.dmd"),
        ("service_debug",           "images/service/debug.dmd"),
        ("service_flashers",        "images/service/flashers.dmd"),
        ("service_font",            "images/service/font.dmd"),
        ("service_game_settings",   "images/service/game_settings.dmd"),
        ("service_lamps",           "images/service/lamps.dmd"),
        ("service_money",           "images/service/money.dmd"),
        ("service_music",           "images/service/music.dmd"),
        ("service_server",          "images/service/server.dmd"),
        ("service_settings",        "images/service/settings.dmd"),
        ("service_sounds",          "images/service/sounds.dmd"),
        ("service_switches",        "images/service/switches.dmd"),
        ("service_tests",           "images/service/tests.dmd"),
        ("service_utilities",       "images/service/utilities.dmd"),
    )
    resources.register_movies(
        ("x2",                      "movies/X2_from_left_ship_from_right - 90-Android.mpg")
    )
    resources.load_sounds(
        ("boot",                "sounds/boot.ogg"),
        ("settings_cleared",    "sounds/settings_cleared.ogg"),
        ("service_cancel",      "sounds/service/cancel.ogg"),
        ("service_enter",       "sounds/service/enter.ogg"),
        ("service_exit",        "sounds/service/exit.ogg"),
        ("service_save",        "sounds/service/save.ogg"),
        ("service_select",      "sounds/service/select.ogg"),
        ("coin_drop",           "sounds/coinDrop.ogg")
    )
    resources.register_music(
        ("introduction", "music/Introduction.ogg", { "start_time": 0.50 }),
        ("credits",      "music/Credits.ogg",      { "start_time": 2.25 })
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
    )
    resources.alias_fonts(
        ("r7b",     "title")
    )
