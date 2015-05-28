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
    devices.add_coils({
        "auto_plunger": {
            "label": "Auto Plunger",
            "device": "02"
        },
        "drop_target_down": {
            "label": "Drop Target, Down",
            "device": "08"
        },
        "drop_target_up": {
            "label": "Drop Target, Up",
            "device": "12"
        },
        "kickback": {
            "label": "Kickback",
            "device": "04"
        },
        "knocker": {
            "label": "Knocker",
            "device": "07"
        },
        "magnet_left": {
            "label": "Magnet, Left",
            "device": "06"
        },
        "magnet_center": {
            "label": "Magnet, Center",
            "device": "05"
        },
        "magnet_right": {
            "label": "Magnet, Right",
            "device": "03"
        },
        "popper": {
            "label": "Popper",
            "device": "01"
        },
        "saucer": {
            "label": "Saucer",
            "device": "15"
        },
        "slingshot_left": {
            "label": "Slingshot, Left",
            "device": "11"
        },
        "slingshot_right": {
            "label": "Slingshot, Right",
            "device": "10"
        },
        "toy": {
            "label": "Toy",
            "device": "16"
        },
        "trough": {
            "label": "Trough",
            "device": "14"
        }
    })
