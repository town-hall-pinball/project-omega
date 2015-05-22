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

from pin.util import Events


dmd = None
"""
TODO
"""

dmd_height = 32
"""
Height of the dot matrix display, in dots.
"""

dmd_width = 128
"""
Width of the dot matrix display, in dots.
"""

dmd_virtual = None
"""
TODO
"""

events = Events()
"""
Global :class:`pin.util.Events` queue
"""

coils = {}
"""
Dictionary of coils/solienoids, keyed by device name.
"""

game = None
"""
TODO
"""

options = None
"""
Dictionary of command line options used when invoking the program, keyed
by option name.
"""

machine = None
"""
TODO
"""

modes = {}
"""
TODO
"""

platform = None
"""
TODO
"""

switches = {}
"""
Dictionary of switches, keyed by device name.
"""
