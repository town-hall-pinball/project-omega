# Copyright (c) 2014 - 2016 townhallpinball.org
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

from ..lib import devices

def init():
    """
    Configures coils for the machine. In the form of::

       devices.add_coils({
            "auto_plunger": {
                "label": "Auto Plunger",
                "device": "C02"
            },
            "drop_target_down": {
                "label": "Drop Target, Down",
                "device": "C08"
            }
        })

    Each coil should be keyed by an identifier (e.g., `auto_plunger`) and
    contain the following:

    - `label`: Descriptive, user-friendly, but not overly verbose description
      of this coil.
    - `device`: A three character code starting with "C" and the number of
      the coil as specified in the owner's manual for the machine.
    """

    devices.add_coils({
        "auto_plunger": {
            "label": "Auto Plunger",
            "device": "C02"
        },
        "drop_target_down": {
            "label": "Drop Target, Down",
            "device": "C08"
        },
        "drop_target_up": {
            "label": "Drop Target, Up",
            "device": "C12"
        },
        "kickback": {
            "label": "Kickback",
            "device": "C04"
        },
        "knocker": {
            "label": "Knocker",
            "device": "C07"
        },
        "magnet_left": {
            "label": "Magnet, Left",
            "device": "C06"
        },
        "magnet_center": {
            "label": "Magnet, Center",
            "device": "C05"
        },
        "magnet_right": {
            "label": "Magnet, Right",
            "device": "C03"
        },
        "popper": {
            "label": "Popper",
            "device": "C01"
        },
        "saucer": {
            "label": "Saucer",
            "device": "C15"
        },
        "slingshot_left": {
            "label": "Slingshot, Left",
            "device": "C11"
        },
        "slingshot_right": {
            "label": "Slingshot, Right",
            "device": "C10"
        },
        "toy": {
            "label": "Toy",
            "device": "C16"
        },
        "trough": {
            "label": "Trough",
            "device": "C14"
        }
    })
