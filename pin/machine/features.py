
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

from ..lib import p, ball, devices, simulator

def init():
    sw = p.switches
    coil = p.coils

    ball.total = 4
    ball.captures = {
        "trough": ball.Capture(
            name="trough",
            switches=[
                sw["trough"],
                sw["trough_2"],
                sw["trough_3"],
                sw["trough_4"]
            ],
            coil=coil["trough"],
            verify={
                "type": "failure",
                "switch": sw["trough_jam"],
                "time": 1.00,
                "retry_time": 3.00
            }
        ),
        "popper": ball.Capture(
            name="popper",
            switches=[
                sw["popper"],
                sw["popper_2"]
            ],
            coil=coil["popper"],
            verify={
                "type": "success",
                "switch": sw["return_right"],
                "time": 1.0
            },
            staged=1
        ),
        "saucer": ball.Capture(
            name="saucer",
            switches=[
                sw["saucer"],
            ],
            coil=coil["saucer"],
            verify={
                "type": "failure",
                "switch": sw["saucer"],
                "time": 1.0
            }
        ),
        "auto_plunger": ball.Capture(
            name="shooter_lane",
            switches=[
                sw["shooter_lane"],
            ],
            coil=coil["auto_plunger"],
        )
    }
    ball.trough = ball.captures["trough"]
    ball.auto_plunger = ball.captures["auto_plunger"]

    ball.shots = {
        "shot_orbit_left": [
            {  "eq": sw["orbit_left"] },
            { "neq": sw["orbit_right"] },
        ],
        "shot_orbit_right": [
            {  "eq": sw["orbit_right"] },
            { "neq": sw["orbit_left"] },
        ],
        "shot_saucer": [
            {   "eq": sw["saucer"] }
        ],
        "shot_subway_left": [
            {  "eq": sw["subway_left"] }
        ],
        "shot_subway_center": [
            {  "eq": sw["subway_center"] },
            { "neq": sw["subway_left"] }
        ],
        "drain": [
            {  "eq": sw["trough_4"] }
        ]
    }

    ball.search_sequence = [
        coil["slingshot_left"],
        coil["slingshot_right"],
        coil["kickback"],
        coil["drop_target_down"],
        coil["drop_target_up"],
        coil["auto_plunger"],
        coil["saucer"],
        coil["popper"],
    ]

    simulator.initial = [
        sw["trough"],
        sw["trough_2"],
        sw["trough_3"],
        sw["popper"]
    ]

    simulator.rules = {
        "coil:trough=pulse": [
            { "from": sw["trough"],     "to": sw["shooter_lane"] },
            { "from": sw["trough_2"],   "to": sw["trough"] },
            { "from": sw["trough_3"],   "to": sw["trough_2"] },
            { "from": sw["trough_4"],   "to": sw["trough_3"] }
        ],
        "switch:trough_4=enable": [
            { "to": sw["trough_4"] },
            { "from": sw["trough_4"],   "to": sw["trough_3"] },
            { "from": sw["trough_3"],   "to": sw["trough_2"] },
            { "from": sw["trough_2"],   "to": sw["trough"] }
        ],
        "coil:auto_plunger=pulse": [
            { "from": sw["shooter_lane"], "hit": sw["slingshot_left"] }
        ],
        "coil:popper=pulse": [
            { "from": sw["popper"] }
        ],
        "switch:subway_left=enable": [
            { "to": sw["subway_center"] }
        ],
        "switch:subway_center=enable": [
            { "from": sw["subway_center"], "to": sw["popper_2"] }
        ],
        "switch:popper_2=enable": [
            { "from": sw["popper_2"], "to": sw["popper"] }
        ],
        "coil:drop_target_up=pulse": [
            { "disable": sw["drop_target"] }
        ]
    }
