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
    devices.add_lamps({
        "ball_launch_button": {
            "label": "Ball Launch Button",
            "device": "86",
        },
        "buy_extra_ball_button": {
            "label": "Buy Extra Ball Button",
            "device": "87",
        },
        "circle_1": {
            "label": "Circle, 01",
            "device": "26",
        },
        "circle_2": {
            "label": "Circle, 02",
            "device": "25",
        },
        "circle_3": {
            "label": "Circle, 03",
            "device": "24",
        },
        "circle_4": {
            "label": "Circle, 04",
            "device": "23",
        },
        "circle_5": {
            "label": "Circle, 05",
            "device": "22",
        },
        "circle_6": {
            "label": "Circle, 06",
            "device": "11",
        },
        "circle_7": {
            "label": "Circle, 07",
            "device": "12",
        },
        "circle_8": {
            "label": "Circle, 08",
            "device": "13",
        },
        "circle_9": {
            "label": "Circle, 09",
            "device": "14",
        },
        "circle_10": {
            "label": "Circle, 10",
            "device": "15",
        },
        "circle_11": {
            "label": "Circle, 11",
            "device": "16",
        },
        "circle_12": {
            "label": "Circle, 12",
            "device": "18",
        },
        "circle_center": {
            "label": "Circle, Center",
            "device": "21",
        },
        "inlane_left": {
            "label": "Inlane, Left",
            "device": "66",
        },
        "inlane_right": {
            "label": "Inlane, Right",
            "device": "73",
        },
        "kickback": {
            "label": "Kickback",
            "device": "68",
        },
        "orbit_left_arrow_1": {
            "label": "Orbit, Left Arrow 1",
            "device": "57"
        },
        "orbit_left_arrow_2": {
            "label": "Orbit, Left Arrow 2",
            "device": "51"
        },
        "orbit_left_circle_3": {
            "label": "Orbit, Left Circle 3",
            "device": "53"
        },
        "orbit_left_sign": {
            "label": "Orbit, Left Sign",
            "device": "38",
        },
        "orbit_right_arrow_1": {
            "label": "Orbit, Right Arrow 1",
            "device": "77",
        },
        "orbit_right_arrow_2": {
            "label": "Orbit, Right Arrow 2",
            "device": "78",
        },
        "outlane_left": {
            "label": "Outlane, Left",
            "device": "67",
        },
        "outlane_right": {
            "label": "Outlane, Right",
            "device": "74",
        },
        "playfield_center": {
            "label": "Playfield, Center",
            "device": "28"
        },
        "playfield_far_left": {
            "label": "Playfield, Far Left",
            "device": "48",
        },
        "playfield_left": {
            "label": "Playfield, Left",
            "device": "17"
        },
        "playfield_right": {
            "label": "Playfield, Right",
            "device": "27"
        },
        "ramp_left_arrow": {
            "label": "Ramp, Left Arrow",
            "device": "56"
        },
        "ramp_left_circle_1": {
            "label": "Ramp, Left Circle 1",
            "device": "55"
        },
        "ramp_left_circle_2": {
            "label": "Ramp, Left Circle 2",
            "device": "52"
        },
        "ramp_left_circle_3": {
            "label": "Ramp, Left Circle 3",
            "device": "54"
        },
        "ramp_left_sign_top": {
            "label": "Ramp, Left Sign Top",
            "device": "84"
        },
        "ramp_left_sign_bottom": {
            "label": "Ramp, Left Sign Bottom",
            "device": "83"
        },
        "ramp_right_arrow_1": {
            "label": "Ramp, Right Arrow 1",
            "device": "75"
        },
        "ramp_right_arrow_2": {
            "label": "Ramp, Right Arrow 2",
            "device": "76"
        },
        "ramp_right_circle_1": {
            "label": "Ramp, Right Circle 1",
            "device": "63",
        },
        "ramp_right_circle_2": {
            "label": "Ramp, Right Circle 2",
            "device": "64",
        },
        "ramp_right_circle_3": {
            "label": "Ramp, Right Circle 3",
            "device": "65",
        },
        "scoop_left_arrow_1": {
            "label": "Scoop, Left Arrow 1",
            "device": "45"
        },
        "scoop_left_arrow_2": {
            "label": "Scoop, Left Arrow 2",
            "device": "46"
        },
        "scoop_left_arrow_3": {
            "label": "Scoop, Left Arrow 3",
            "device": "47",
        },
        "scoop_center_arrow_1": {
            "label": "Scoop, Center Arrow 1",
            "device": "31"
        },
        "scoop_center_arrow_2": {
            "label": "Scoop, Center Arrow 2",
            "device": "33"
        },
        "scoop_center_arrow_3": {
            "label": "Scoop, Center Arrow 3",
            "device": "34"
        },
        "scoop_center_arrow_4": {
            "label": "Scoop, Center Arrow 4",
            "device": "36"
        },
        "scoop_center_circle": {
            "label": "Scoop, Center Circle",
            "device": "35"
        },
        "shoot_again": {
            "label": "Shoot Again",
            "device": "81"
        },
        "standup_target_bottom": {
            "label": "Standup Target, Bottom",
            "device": "72"
        },
        "standup_target_top": {
            "label": "Standup Target, Top",
            "device": "71"
        },
        "start_button": {
            "label": "Start Button",
            "device": "88",
        },
        "toy_left": {
            "label": "Toy, Left",
            "device": "82",
        },
        "toy_right": {
            "label": "Toy, Right",
            "device": "85"
        },
        "u_turn_left_arrow": {
            "label": "U-Turn, Left Arrow",
            "device": "41"
        },
        "u_turn_left_circle_1": {
            "label": "U-Turn, Left Circle 1",
            "device": "42"
        },
        "u_turn_left_circle_2": {
            "label": "U-Turn, Left Circle 2",
            "device": "43"
        },
        "u_turn_left_circle_3": {
            "label": "U-Turn, Left Circle 3",
            "device": "44"
        },
        "u_turn_right_arrow": {
            "label": "U-Turn, Right Arrow",
            "device": "32"
        }
    })
