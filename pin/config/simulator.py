
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

from ..lib import p, simulator

def init():
    sw = p.switches

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
            { "from": sw["popper"],     "hit": sw["return_right"] },
            { "from": sw["popper_2"],   "to": sw["popper"]}
        ],
        "switch:subway_left=enable": [
            { "to": sw["popper_2"] },
        ],
        "switch:subway_center=enable": [
            { "to": sw["popper_2"] }
        ],
        "switch:popper_2=enable": [
            { "from": sw["popper_2"], "to": sw["popper"] }
        ],
        "coil:drop_target_up=pulse": [
            { "disable": sw["drop_target"] }
        ]
    }
