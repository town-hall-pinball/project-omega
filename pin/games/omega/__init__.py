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

from . import attract, system
from ... import resources

def init():
    resources.load_fonts(
        ("titlel",    "fonts/pf_tempesta_five_extended_bold.ttf", 8),
        ("titlek",    "fonts/pf_tempesta_five_extended.ttf", 8),
        ("titlej",    "fonts/pf_tempesta_five_condensed_bold.ttf", 8),
        ("titlei",    "fonts/pf_tempesta_five_condensed.ttf", 8),
        ("titleh",    "fonts/pf_tempesta_five_compressed_bold.ttf", 8),
        ("titleg",    "fonts/pf_tempesta_five_compressed.ttf", 8),
        ("titlef",    "fonts/pf_tempesta_five_bold.ttf", 8),
        ("titlee",    "fonts/pf_tempesta_five.ttf", 8),
        ("title",    "fonts/pf_ronda_seven_bold.ttf", 8),
        #("title",    "fonts/pf_ronda_seven.ttf", 8),
        ("titleb",    "fonts/pf_arma_five.ttf", 8),
        ("titlea",    "fonts/PetMe128.ttf", 8),
    )
    resources.load_images(
        ("thp_logo", "images/thp_logo.dmd"),
    )

    system.init()
    attract.init()

    system.mode.enable()
    attract.mode.enable()
