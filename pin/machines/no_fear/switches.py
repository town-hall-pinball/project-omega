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

from ... import devices

def init():
    devices.add_switches({
        "ball_launch_button": {
            "label": "Ball Launch Button",
            "device": "11",
        },
        "buy_extra_ball_button": {
            "label": "Buy Extra Ball Button",
            "device": "23",
        },
        "coin_door": {
            "label": "Coin Door",
            "device": "D1",
        },
        "coin_left": {
            "label": "Coin, Left",
            "device": "D1",
        },
        "coin_center": {
            "label": "Coin, Center",
            "device": "D2"
        },
        "coin_right": {
            "label": "Coin, Right",
            "device": "D3"
        },
        "coin_fourth": {
            "label": "Coin, Fourth",
            "device": "D4",
        },
        "drop_target": {
            "label": "Drop Target",
            "device": "51",
        },
        "flipper_left": {
            "label": "Flipper, Left",
            "device": "F4",
        },
        "flipper_right": {
            "label": "Flipper, Right",
            "device": "F2",
        },
        "flipper_right_up": {
            "label": "Flipper, Upper Right",
            "device": "F6",
        },
        "kickback": {
            "label": "Kickback",
            "device": "25",
        },
        "magnet_left": {
            "label": "Magnet, Left",
            "device": "47",
            "opto": True,
        },
        "magnet_center": {
            "label": "Magnet, Center",
            "device": "47",
            "opto": True,
        },
        "magnet_right": {
            "label": "Magnet, Right",
            "device": "48",
            "opto": True,
        },
        "orbit_left": {
            "label": "Orbit, Left",
            "device": "62",
        },
        "orbit_right": {
            "label": "Orbit, Right",
            "device": "58",
        },
        "outlane_right": {
            "label": "Outlane, Right",
            "device": "17",
        },
        "popper": {
            "label": "Popper",
            "device": "41",
            "opto": True,
        },
        "popper_2": {
            "label": "Popper, #2",
            "device": "42",
            "opto": True,
        },
        "ramp_left_enter": {
            "label": "Ramp, Left Enter",
            "device": "63",
        },
        "ramp_left_middle": {
            "label": "Ramp, Left Middle",
            "device": "64",
        },
        "ramp_right_enter": {
            "label": "Ramp, Right Enter",
            "device": "66",
        },
        "ramp_right_exit": {
            "label": "Ramp, Right Exit",
            "device": "67",
        },
        "return_left": {
            "label": "Return, Left",
            "device": "26",
        },
        "return_right": {
            "label": "Return, Right",
            "device": "18",
        },
        "saucer": {
            "label": "Saucer",
            "device": "61",
        },
        "service_down": {
            "label": "Service, Down",
            "device": "D6"
        },
        "service_enter": {
            "label": "Service, Enter",
            "device": "D8",
        },
        "service_exit": {
            "label": "Service, Exit",
            "device": "D5",
        },
        "service_up": {
            "label": "Service, Up",
            "device": "D7",
        },
        "shooter_lane": {
            "label": "Shooter Lane",
            "device": "15",
        },
        "slingshot_left": {
            "label": "Slingshot, Left",
            "device": "27",
        },
        "slingshot_right": {
            "label": "Slingshot, Right",
            "device": "28",
        },
        "spinner": {
            "label": "Spinner",
            "device": "16",
        },
        "standup_target_bottom": {
            "label": "Standup Target, Bottom",
            "device": "56",
        },
        "startup_target_top": {
            "label": "Standup Target, Top",
            "device": "57",
        },
        "start_button": {
            "label": "Start Button",
            "device": "13",
        },
        "subway_left": {
            "label": "Subway, Left",
            "device": "38",
            "opto": True,
        },
        "subway_center": {
            "label": "Subway, Center",
            "device": "37",
            "opto": True,
        },
        "tilt": {
            "label": "Tilt",
            "device": "14",
            "opto": True,
        },
        "tilt_slam": {
            "label": "Tilt, Slam",
            "device": "21",
        },
        "trough_jam": {
            "label": "Trough, Jam",
            "device": "31",
            "opto": True,
        },
        "trough": {
            "label": "Trough",
            "device": "32",
            "opto": True,
        },
        "trough_2": {
            "label": "Trough, 2",
            "device": "33",
            "opto": True
        },
        "trough_3": {
            "label": "Trough, 3",
            "device": "34",
            "opto": True,
        },
        "trough_4": {
            "label": "Trough, 4",
            "device": "35",
            "opto": True
        },
        "u_turn": {
            "label": "U-Turn",
            "device": "55",
            "opto": True,
        },
        "wireform_left": {
            "label": "Wireform, Left",
            "device": "54",
        }
   })

