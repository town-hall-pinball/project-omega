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

from pin.lib import keyboard
from pin.lib.keyboard import event, switch

def init():
    keyboard.register({
        "d": switch("trough_4"),
        "s": switch("saucer"),
    "space": switch("start_button"),
       "cs": switch("buy_extra_ball_button"),
        "l": switch("ball_launch_button"),
        "1": switch("coin_left"),
        "7": switch("service_enter"),
        "8": switch("service_down"),
        "9": switch("service_up"),
        "0": switch("service_exit"),
        "[": switch("flipper_left"),
        "]": switch("flipper_right"),
        ",": switch("slingshot_left"),
        ".": switch("slingshot_right"),
        "m": switch("subway_center"),
        "n": switch("subway_left"),
        "z": switch("tilt"),
        "x": switch("tilt_slam"),
    })

