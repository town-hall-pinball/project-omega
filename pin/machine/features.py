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

import p
from pin import ball

def init():
    ball.total = 4
    ball.captures = {
        "trough": ball.Capture(
            name="trough",
            switches=[
                p.switches["trough"],
                p.switches["trough_2"],
                p.switches["trough_3"],
                p.switches["trough_4"]
            ],
            coil="trough",
            verify={
                "type": "failure",
                "switch": p.switches["trough_jam"],
                "time": 1.0
            }
        ),
        "popper": ball.Capture(
            name="popper",
            switches=[
                "popper",
                "popper_2"
            ],
            coil="popper",
            verify={
                "type": "success",
                "switch": p.switches["return_right"],
                "time": 1.0
            },
            staged=1
        ),
        "saucer": ball.Capture(
            name="saucer",
            switches=["saucer"],
            coil="saucer",
            verify={
                "type": "failure",
                "switch": "saucer",
                "time": 1.0
            }
        ),
        "shooter_lane": ball.Capture(
            name="shooter_lane",
            switches=["shooter_lane"],
            coil="auto_plunger",
            verify={
                "type": "failure",
                "switch": "shooter_lane",
                "time": 1.0
            }
        )
    }

    ball.search_sequence = [
        p.coils["slingshot_left"],
        p.coils["slingshot_right"],
        p.coils["kickback"],
        p.coils["drop_target_down"],
        p.coils["drop_target_up"],
        p.coils["auto_plunger"],
        p.coils["saucer"],
        p.coils["popper"],
    ]
