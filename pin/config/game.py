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

from ..lib import p, ball
from ..lib.game import Game as BaseGame

class Game(BaseGame):

    def setup(self):
        super(Game, self).setup()

        self.flippers = p.modes["flippers"]
        self.kickback = p.modes["kickback"]
        self.magnets = p.modes["magnets"]
        self.plunger = p.modes["plunger"]
        self.slingshots = p.modes["slingshots"]
        self.trough = p.modes["trough"]

        self.handlers += [
            self.flippers,
            self.kickback,
            self.magnets,
            self.plunger,
            self.slingshots,
            self.trough
        ]


    def playfield_enable(self):
        """
        #if self.playfield_enabled:
        #    return
        p.coils["slingshot_left"].auto_pulse(p.switches["slingshot_left"])
        p.coils["slingshot_right"].auto_pulse(p.switches["slingshot_right"])
        self.flippers_enable()
        """
        self.playfield_enabled = True
        p.events.post("playfield_enable")

    def playfield_disable(self):
        """
        #if not self.playfield_enabled:
        #    return
        p.coils["slingshot_left"].auto_cancel()
        p.coils["slingshot_right"].auto_cancel()
        self.kickback_disable()
        self.magnets_disable()
        self.flippers_disable()
        """
        self.playfield_enabled = False
        p.events.post("playfield_disable")
