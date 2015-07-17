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
    devices.add_lamps({
        "ball_launch_button": {
            "label": "Ball Launch Button",
            "device": "L86",
        },
        "buy_extra_ball_button": {
            "label": "Buy Extra Ball Button",
            "device": "L87",
        },
        "circle_1": {
            "label": "Circle, 01",
            "device": "L26",
        },
        "circle_2": {
            "label": "Circle, 02",
            "device": "L25",
        },
        "circle_3": {
            "label": "Circle, 03",
            "device": "L24",
        },
        "circle_4": {
            "label": "Circle, 04",
            "device": "L23",
        },
        "circle_5": {
            "label": "Circle, 05",
            "device": "L22",
        },
        "circle_6": {
            "label": "Circle, 06",
            "device": "L11",
        },
        "circle_7": {
            "label": "Circle, 07",
            "device": "L12",
        },
        "circle_8": {
            "label": "Circle, 08",
            "device": "L13",
        },
        "circle_9": {
            "label": "Circle, 09",
            "device": "L14",
        },
        "circle_10": {
            "label": "Circle, 10",
            "device": "L15",
        },
        "circle_11": {
            "label": "Circle, 11",
            "device": "L16",
        },
        "circle_12": {
            "label": "Circle, 12",
            "device": "L18",
        },
        "circle_center": {
            "label": "Circle, Center",
            "device": "L21",
        },
        "inlane_left": {
            "label": "Inlane, Left",
            "device": "L66",
        },
        "inlane_right": {
            "label": "Inlane, Right",
            "device": "L73",
        },
        "kickback": {
            "label": "Kickback",
            "device": "L68",
        },
        "orbit_left_arrow_1": {
            "label": "Orbit, Left Arrow 1",
            "device": "L57"
        },
        "orbit_left_arrow_2": {
            "label": "Orbit, Left Arrow 2",
            "device": "L51"
        },
        "orbit_left_circle_3": {
            "label": "Orbit, Left Circle 3",
            "device": "L53"
        },
        "orbit_left_sign": {
            "label": "Orbit, Left Sign",
            "device": "L38",
        },
        "orbit_right_arrow_1": {
            "label": "Orbit, Right Arrow 1",
            "device": "L77",
        },
        "orbit_right_arrow_2": {
            "label": "Orbit, Right Arrow 2",
            "device": "L78",
        },
        "outlane_left": {
            "label": "Outlane, Left",
            "device": "L67",
        },
        "outlane_right": {
            "label": "Outlane, Right",
            "device": "L74",
        },
        "playfield_center": {
            "label": "Playfield, Center",
            "device": "L28"
        },
        "playfield_far_left": {
            "label": "Playfield, Far Left",
            "device": "L48",
        },
        "playfield_left": {
            "label": "Playfield, Left",
            "device": "L17"
        },
        "playfield_right": {
            "label": "Playfield, Right",
            "device": "L27"
        },
        "ramp_left_arrow": {
            "label": "Ramp, Left Arrow",
            "device": "L56"
        },
        "ramp_left_circle_1": {
            "label": "Ramp, Left Circle 1",
            "device": "L55"
        },
        "ramp_left_circle_2": {
            "label": "Ramp, Left Circle 2",
            "device": "L52"
        },
        "ramp_left_circle_3": {
            "label": "Ramp, Left Circle 3",
            "device": "L54"
        },
        "ramp_left_sign_top": {
            "label": "Ramp, Left Sign Top",
            "device": "L84"
        },
        "ramp_left_sign_bottom": {
            "label": "Ramp, Left Sign Bottom",
            "device": "L83"
        },
        "ramp_right_arrow_1": {
            "label": "Ramp, Right Arrow 1",
            "device": "L75"
        },
        "ramp_right_arrow_2": {
            "label": "Ramp, Right Arrow 2",
            "device": "L76"
        },
        "ramp_right_circle_1": {
            "label": "Ramp, Right Circle 1",
            "device": "L63",
        },
        "ramp_right_circle_2": {
            "label": "Ramp, Right Circle 2",
            "device": "L64",
        },
        "ramp_right_circle_3": {
            "label": "Ramp, Right Circle 3",
            "device": "L65",
        },
        "saucer_arrow_1": {
            "label": "Saucer, Arrow 1",
            "device": "L61"
        },
        "saucer_arrow_2": {
            "label": "Saucer, Arrow 2",
            "device": "L62",
        },
        "scoop_left_arrow_1": {
            "label": "Scoop, Left Arrow 1",
            "device": "L45"
        },
        "scoop_left_arrow_2": {
            "label": "Scoop, Left Arrow 2",
            "device": "L46"
        },
        "scoop_left_arrow_3": {
            "label": "Scoop, Left Arrow 3",
            "device": "L47",
        },
        "scoop_center_arrow_1": {
            "label": "Scoop, Center Arrow 1",
            "device": "L31"
        },
        "scoop_center_arrow_2": {
            "label": "Scoop, Center Arrow 2",
            "device": "L33"
        },
        "scoop_center_arrow_3": {
            "label": "Scoop, Center Arrow 3",
            "device": "L34"
        },
        "scoop_center_arrow_4": {
            "label": "Scoop, Center Arrow 4",
            "device": "L36"
        },
        "scoop_center_circle": {
            "label": "Scoop, Center Circle",
            "device": "L35"
        },
        "shoot_again": {
            "label": "Shoot Again",
            "device": "L81"
        },
        "standup_target_bottom": {
            "label": "Standup Target, Bottom",
            "device": "L72"
        },
        "standup_target_top": {
            "label": "Standup Target, Top",
            "device": "L71"
        },
        "start_button": {
            "label": "Start Button",
            "device": "L88",
        },
        "toy_left": {
            "label": "Toy, Left",
            "device": "L82",
        },
        "toy_right": {
            "label": "Toy, Right",
            "device": "L85"
        },
        "u_turn_left_arrow": {
            "label": "U-Turn, Left Arrow",
            "device": "L41"
        },
        "u_turn_left_circle_1": {
            "label": "U-Turn, Left Circle 1",
            "device": "L42"
        },
        "u_turn_left_circle_2": {
            "label": "U-Turn, Left Circle 2",
            "device": "L43"
        },
        "u_turn_left_circle_3": {
            "label": "U-Turn, Left Circle 3",
            "device": "L44"
        },
        "u_turn_right_arrow": {
            "label": "U-Turn, Right Arrow",
            "device": "L32"
        }
    })
