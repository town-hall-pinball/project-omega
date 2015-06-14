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

settings = {
    "name": "Settings",
    "icon": "service_settings",
    "menu": [{
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
            ]}
        ]
    },{
        "name": "Gameplay",
        "icon": "service_game_settings",
        "menu": [{
            "name": "Tilt Warnings",
            "data": "tilt_warnings",
            "options": [
                [ 1, "1" ],
                [ 2, "2" ],
                [ 3, "3" ],
                [ 4, "4" ],
            ]}
        ]
    }]
}


tests = {
    "name": "Tests",
    "icon": "service_tests",
    "menu": [{
        "name": "Switches",
        "icon": "service_switches",
        "action": "switch_test"
    },{
        "name": "Coils",
        "icon": "service_coils",
        "action": "coil_test"
    },{
        "name": "Lamps",
        "icon": "service_lamps",
        "menu": [{
            "name": "All",
            "action": "lamp_test_all"
        },{
            "name": "Individual",
            "action": "lamp_test_individual"
        }]
    },{
        "name": "Flashers",
        "icon": "service_flashers",
        "menu": [{
            "name": "All",
            "event": "flasher_test_all"
        },{
            "name": "Individual",
            "event": "flasher_test_individual"
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
        "name": "Browser",
        "icon": "service_browse",
        "menu": [{
            "name": "Animations",
            "icon": "service_animations",
            "action": "animation_browser"
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
