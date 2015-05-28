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
    devices.add_flashers({
        "auto_fire": {
            "label": "Auto Fire",
            "device": "C25",
        },
        "circle_center": {
            "label": "Circle, Center",
            "device": "C19",
        },
        "flipper_return": {
            "label": "Flipper Return",
            "device": "C17",
        },
        "insert_explode": {
            "label": "Insert, Explode",
            "device": "C22",
        },
        "insert_top_left": {
            "label": "Insert, Top Left",
            "device": "C26",
        },
        "insert_top_right": {
            "label": "Insert, Top Right",
            "device": "C27",
        },
        "outside": {
            "label": "Outside",
            "device": "C24",
        },
        "popper": {
            "label": "Popper",
            "device": "C28",
        },
        "ramp_left": {
            "label": "Ramp, Left",
            "device": "C23",
        },
        "ramp_right": {
            "label": "Ramp, Right",
            "device": "C20",
        },
        "toy": {
            "label": "Toy",
            "device": "C21",
        },
        "spinner": {
            "label": "Spinner",
            "device": "C18",
        },
    })
