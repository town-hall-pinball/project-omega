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

__all__ = ["main"]

game_pricing = {
    "name": "Pricing",
    "icon": "service_money",
    "menu": [{
        "name": "Free Play",
        "data": "free_play",
        "options": [
            [True, "Yes"],
            [False, "No"],
        ]},{
        "name": "Game Pricing",
        "data": "pricing",
        "options": [
            [ 0.25,  "1 for 0.25" ],
            [ 0.50,  "1 for 0.50" ],
            [ 0.75,  "1 for 0.75" ],
            [ 1.00,  "1 for 1.00" ],
        ]
    }]
}

general_gameplay = {
    "name": "General",
    "menu": [{
        "name": "Tilt Warnings",
        "data": "tilt_warnings",
        "options": [
            [ 1, "1" ],
            [ 2, "2" ],
            [ 3, "3" ],
            [ 4, "4" ],
        ]
    }]
}

practice_gameplay = {
    "name": "Practice",
    "menu": [{
        "name": "Timer",
        "data": "practice_timer",
        "options": [
            [5,     "0:05"],
            [60,    "1:00"],
            [120,   "2:00"],
            [180,   "3:00"],
            [240,   "4:00"],
            [300,   "5:00"],
            [6000,  "10:00"]
        ]}
    ]
}

general = {
    "name": "General",
    "icon": "service_settings",
    "menu": [{
        "name": "Power Save",
        "data": "power_save_timer",
        "options": [
            [5,         "0:05"],
            [2 * 60,    "2:00"],
            [5 * 60,    "5:00"],
            [10 * 60,  "10:00"]
        ]}
    ]
}

gameplay = {
    "name": "Gameplay",
    "icon": "service_game_settings",
    "menu": [
        general_gameplay,
        practice_gameplay
    ]
}

settings = {
    "name": "Settings",
    "icon": "service_settings",
    "menu": [
        general,
        gameplay,
        game_pricing,
    ]
}

tests = {
    "name": "Tests",
    "icon": "service_tests",
    "menu": [{
        "name": "Switches",
        "icon": "service_switches",
        "menu": [{
            "name": "Test Edges",
            "action": "switch_edges_test"
        },{
            "name": "Test Levels",
            "action": "switch_levels_test"
        },{
            "name": "Test Single",
            "action": "switch_single_test"
        }],
    },{
        "name": "Coils",
        "icon": "service_coils",
        "action": "coils_test"
    },{
        "name": "Lights",
        "icon": "service_lamps",
        "menu": [{
            "name": "Test All Lamps",
            "action": "lamps_all_test"
        },{
            "name": "Test Single Lamps",
            "action": "lamps_single_test"
        },{
            "name": "Test All Flashers",
            "action": "flashers_all_test"
        },{
            "name": "Test Single Flashers",
            "action": "flashers_single_test"
        }]
    },{
        "name": "Flippers",
        "icon": "service_flippers",
        "action": "flippers_test"
    },{
        "name": "More...",
        "icon": "service_more",
        "menu": [{
        }]
    }]
}

audits = {
    "name": "Audits",
    "icon": "service_audits",
    "menu": [{
        "name": "Earnings",
        "data": "earnings",
        "format": "{:.2f}"
    },{
        "name": "Paid Credits",
        "data": "paid_credits"
    },{
        "name": "Service Credits",
        "data": "service_credits"
    }]
}

utilities = {
    "name": "Utilities",
    "icon": "service_utilities",
    "menu": [{
        "name": "Server",
        "icon": "service_server",
        "menu": [{
            "name": "Enable Server",
            "data": "server_enabled",
            "options": [
                [True, "Yes"],
                [False, "No"]
            ]
        },{
            "name": "Publish Events",
            "data": "server_publish_events",
            "options": [
                [True, "Yes"],
                [False, "No"]
            ]
        },{
            "name": "Remote Control",
            "data": "server_remote_control",
            "options": [
                [True, "Yes"],
                [False, "No"]
            ]
        }]
    },{
        "name": "Clear",
        "icon": "service_clear",
        "menu": [{
            "name": "Credits",
            "action": "clear_credits",
            "confirm": True
        },{
            "name": "Audits",
            "action": "clear_audits",
            "confirm": True
        }]
    },{
        "name": "Browsers",
        "icon": "service_browse",
        "menu": [{
            "name": "Music",
            "icon": "service_music",
            "action": "music_browser",
        },{
            "name": "Sounds",
            "icon": "service_sounds",
            "action": "sound_browser"
        },{
            "name": "Fonts",
            "icon": "service_font",
            "action": "font_browser",
        },{
            "name": "Images",
            "icon": "service_image",
            "action": "image_browser"
        },{
            "name": "Movies",
            "icon": "service_animations",
            "action": "movie_browser"
        }]
    },{
        "name": "Debug",
        "icon": "service_debug",
        "menu": [{
            "name": "Simulator",
            "data": "simulator_enabled",
            "options": [
                [True, "Yes"],
                [False, "No"]
            ],
        }]
    },{
        "name": "More...",
        "icon": "service_more",
        "menu": [{
            "name": "Virtual Palette",
            "action": "virtual_palette"
        }]
    }]
}

main = {
    "name": "Service",
    "menu": [
        settings,
        tests,
        audits,
        utilities
    ]
}
