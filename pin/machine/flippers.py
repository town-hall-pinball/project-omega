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
    devices.add_flippers({
        "left": {
            "label": "Flipper, Left",
            "device": "flipper_lower_left_main",
            "hold_device": "flipper_lower_left_hold",
            "switch": "flipper_left"
        },
        "right": {
            "label": "Flipper, Right",
            "device": "flipper_lower_right_main",
            "hold_device": "flipper_lower_right_hold",
            "switch": "flipper_right"
        },
        "right_up": {
            "label": "Flipper, Right Upper",
            "device": "flipper_upper_right_main",
            "hold_device": "flipper_upper_right_hold",
            "switch": "flipper_right_up"
        }
    })


