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

from pin.lib import proc

dmd_enabled = False

def reset(*args, **kwargs):
    pass

def get_events():
    return [{"type": proc.DMD_READY}] if dmd_enabled else []

def switch_update_rule(*args, **kwargs):
    pass

def flush():
    pass

def watchdog_tickle():
    pass

def dmd_draw(*args, **kwargs):
    pass

def driver_pulse(*args, **kwargs):
    pass

def driver_state_pulse(*args, **kwargs):
    pass

def driver_disable(*args, **kwargs):
    pass

def driver_state_disable(*args, **kwargs):
    pass

def driver_patter(*args, **kwargs):
    pass

def driver_state_patter(*args, **kwargs):
    pass

def driver_get_state(*args, **kwargs):
    pass



