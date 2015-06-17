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

from .. import devices

def init():
    devices.add_switches({
        "ball_launch_button": {
            "label": "Ball Launch Button",
            "device": "S11",
        },
        "buy_extra_ball_button": {
            "label": "Buy Extra Ball Button",
            "device": "S23",
        },
        "coin_door": {
            "label": "Coin Door",
            "device": "S22",
        },
        "coin_left": {
            "label": "Coin, Left",
            "device": "SD1",
        },
        "coin_center": {
            "label": "Coin, Center",
            "device": "SD2"
        },
        "coin_right": {
            "label": "Coin, Right",
            "device": "SD3"
        },
        "coin_fourth": {
            "label": "Coin, Fourth",
            "device": "SD4",
        },
        "drop_target": {
            "label": "Drop Target",
            "device": "S51",
        },
        "flipper_left": {
            "label": "Flipper, Left",
            "device": "SF4",
        },
        "flipper_right": {
            "label": "Flipper, Right",
            "device": "SF2",
        },
        "flipper_right_up": {
            "label": "Flipper, Upper Right",
            "device": "SF6",
        },
        "kickback": {
            "label": "Kickback",
            "device": "S25",
        },
        "magnet_left": {
            "label": "Magnet, Left",
            "device": "S46",
            "opto": True,
        },
        "magnet_center": {
            "label": "Magnet, Center",
            "device": "S47",
            "opto": True,
        },
        "magnet_right": {
            "label": "Magnet, Right",
            "device": "S48",
            "opto": True,
        },
        "orbit_left": {
            "label": "Orbit, Left",
            "device": "S62",
        },
        "orbit_right": {
            "label": "Orbit, Right",
            "device": "S58",
        },
        "outlane_right": {
            "label": "Outlane, Right",
            "device": "S17",
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
        },
        "ramp_left_enter": {
            "label": "Ramp, Left Enter",
            "device": "S63",
        },
        "ramp_left_middle": {
            "label": "Ramp, Left Middle",
            "device": "S64",
        },
        "ramp_right_enter": {
            "label": "Ramp, Right Enter",
            "device": "S66",
        },
        "ramp_right_exit": {
            "label": "Ramp, Right Exit",
            "device": "S67",
        },
        "return_left": {
            "label": "Return, Left",
            "device": "S26",
        },
        "return_right": {
            "label": "Return, Right",
            "device": "S18",
        },
        "saucer": {
            "label": "Saucer",
            "device": "S61",
        },
        "service_down": {
            "label": "Service, Down",
            "device": "SD6"
        },
        "service_enter": {
            "label": "Service, Enter",
            "device": "SD8",
        },
        "service_exit": {
            "label": "Service, Exit",
            "device": "SD5",
        },
        "service_up": {
            "label": "Service, Up",
            "device": "SD7",
        },
        "shooter_lane": {
            "label": "Shooter Lane",
            "device": "S15",
        },
        "slingshot_left": {
            "label": "Slingshot, Left",
            "device": "S27",
        },
        "slingshot_right": {
            "label": "Slingshot, Right",
            "device": "S28",
        },
        "spinner": {
            "label": "Spinner",
            "device": "S16",
        },
        "standup_target_bottom": {
            "label": "Standup Target, Bottom",
            "device": "S56",
        },
        "startup_target_top": {
            "label": "Standup Target, Top",
            "device": "S57",
        },
        "start_button": {
            "label": "Start Button",
            "device": "S13",
        },
        "subway_left": {
            "label": "Subway, Left",
            "device": "S38",
            "opto": True,
        },
        "subway_center": {
            "label": "Subway, Center",
            "device": "S37",
            "opto": True,
        },
        "tilt": {
            "label": "Tilt",
            "device": "S14",
            "opto": True,
        },
        "tilt_slam": {
            "label": "Tilt, Slam",
            "device": "S21",
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
            "opto": True,
        },
        "wireform_left": {
            "label": "Wireform, Left",
            "device": "S54",
        }
   })

