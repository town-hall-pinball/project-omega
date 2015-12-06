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

from ..lib import devices

def init():
    devices.add_switches({
        "ball_launch_button": {
            "label": "Ball Launch Button",
            "device": "S11",
            "tags": ["user"]
        },
        "buy_extra_ball_button": {
            "label": "Buy Extra Ball Button",
            "device": "S23",
            "tags": ["user"],
        },
        "coin_door": {
            "label": "Coin Door",
            "device": "S22",
            "tags": ["user"],
        },
        "coin_left": {
            "label": "Coin, Left",
            "device": "SD1",
            "tags": ["user"],
        },
        "coin_center": {
            "label": "Coin, Center",
            "device": "SD2",
            "tags": ["user"],
        },
        "coin_right": {
            "label": "Coin, Right",
            "device": "SD3",
            "tags": ["user"],
        },
        "coin_fourth": {
            "label": "Coin, Fourth",
            "device": "SD4",
            "tags": ["user"],
        },
        "drop_target": {
            "label": "Drop Target",
            "device": "S51",
            "tags": ["live"],
        },
        "flipper_left": {
            "label": "Flipper, Left",
            "device": "SF4",
            "tags": ["user"]
        },
        "flipper_right": {
            "label": "Flipper, Right",
            "device": "SF2",
            "tags": ["user"]
        },
        "flipper_right_up": {
            "label": "Flipper, Upper Right",
            "device": "SF6",
            "tags": ["user"],
        },
        "kickback": {
            "label": "Kickback",
            "device": "S25",
            "tags": ["live"],
        },
        "magnet_left": {
            "label": "Magnet, Left",
            "device": "S46",
            "opto": True,
            "tags": ["live"],
        },
        "magnet_center": {
            "label": "Magnet, Center",
            "device": "S47",
            "opto": True,
            "tags": ["live"],
        },
        "magnet_right": {
            "label": "Magnet, Right",
            "device": "S48",
            "opto": True,
            "tags": ["live"],
        },
        "orbit_left": {
            "label": "Orbit, Left",
            "device": "S62",
            "tags": ["live"],
        },
        "orbit_right": {
            "label": "Orbit, Right",
            "device": "S58",
            "tags": ["live"],
        },
        "outlane_right": {
            "label": "Outlane, Right",
            "device": "S17",
            "tags": ["live"],
        },
        "popper": {
            "label": "Popper",
            "device": "S41",
            "opto": True,
        },
        "popper_2": {
            "label": "Popper, #2",
            "device": "S42",
            "opto": True,
            "tags": ["live"],
        },
        "ramp_left_enter": {
            "label": "Ramp, Left Enter",
            "device": "S63",
            "tags": ["live"],
        },
        "ramp_left_middle": {
            "label": "Ramp, Left Middle",
            "device": "S64",
            "tags": ["live"],
        },
        "ramp_right_enter": {
            "label": "Ramp, Right Enter",
            "device": "S66",
            "tags": ["live"],
        },
        "ramp_right_exit": {
            "label": "Ramp, Right Exit",
            "device": "S67",
            "tags": ["live"],
        },
        "return_left": {
            "label": "Return, Left",
            "device": "S26",
            "tags": ["live"],
        },
        "return_right": {
            "label": "Return, Right",
            "device": "S18",
            "tags": ["live"],
        },
        "saucer": {
            "label": "Saucer",
            "device": "S61",
            "tags": ["live"],
        },
        "service_down": {
            "label": "Service, Down",
            "device": "SD6",
            "tags": ["user"],
        },
        "service_enter": {
            "label": "Service, Enter",
            "device": "SD8",
            "tags": ["user"],
        },
        "service_exit": {
            "label": "Service, Exit",
            "device": "SD5",
            "tags": ["user"],
        },
        "service_up": {
            "label": "Service, Up",
            "device": "SD7",
            "tags": ["user"],
        },
        "shooter_lane": {
            "label": "Shooter Lane",
            "device": "S15",
        },
        "slingshot_left": {
            "label": "Slingshot, Left",
            "device": "S27",
            "tags": ["live"],
        },
        "slingshot_right": {
            "label": "Slingshot, Right",
            "device": "S28",
            "tags": ["live"],
        },
        "spinner": {
            "label": "Spinner",
            "device": "S16",
            "tags": ["live"],
        },
        "standup_target_bottom": {
            "label": "Standup Target, Bottom",
            "device": "S56",
            "tags": ["live"],
        },
        "startup_target_top": {
            "label": "Standup Target, Top",
            "device": "S57",
            "tags": ["live"],
        },
        "start_button": {
            "label": "Start Button",
            "device": "S13",
            "tags": ["user"]
        },
        "subway_left": {
            "label": "Subway, Left",
            "device": "S38",
            "opto": True,
            "tags": ["live"],
        },
        "subway_center": {
            "label": "Subway, Center",
            "device": "S37",
            "opto": True,
            "tags": ["live"],
        },
        "tilt": {
            "label": "Tilt",
            "device": "S14",
            "tags": ["user"],
        },
        "tilt_slam": {
            "label": "Tilt, Slam",
            "device": "S21",
            "tags": ["user"],
        },
        "trough_jam": {
            "label": "Trough, Jam",
            "device": "S31",
            "opto": True,
        },
        "trough": {
            "label": "Trough",
            "device": "S32",
            "opto": True,
        },
        "trough_2": {
            "label": "Trough, 2",
            "device": "S33",
            "opto": True
        },
        "trough_3": {
            "label": "Trough, 3",
            "device": "S34",
            "opto": True,
        },
        "trough_4": {
            "label": "Trough, 4",
            "device": "S35",
            "opto": True
        },
        "u_turn": {
            "label": "U-Turn",
            "device": "S55",
            "tags": ["live"],
        },
        "wireform_left": {
            "label": "Wireform, Left",
            "device": "S54",
            "tags": ["live"],
        }
    })


