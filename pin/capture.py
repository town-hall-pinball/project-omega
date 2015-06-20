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

import logging

log = logging.getLogger("pin.capture")

class BallCapture(object):

    def __init__(self, name, switches, eject_coil):
        self.name = name
        self.switches = switches
        self.eject_coil = eject_coil

    def capacity(self):
        return len(self.switches)

    def balls(self):
        balls = 0
        for switch in self.switches:
            if switch.active:
                balls =+ 1
        return balls

    def eject(self):
        if self.balls() > 0:
            log.debug("Ejecting {}".format(name))
            self.eject_coil.pulse()
        else:
            log.warn("No balls to eject in {}".format(self.name))


class Trough(BallCapture):

    def __init__(self, switches, jam_switch="trough_jam", eject_coil="trough",
                shooter_lane="shooter_lane"):
        super(Trough, self).__init__("trough", switches, jam_switch, eject_coil)
        self.jam_switch = jam_switch
        self.shooter_lane = shooter_lane




