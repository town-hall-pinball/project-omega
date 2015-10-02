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

from ..lib import p
from ..lib.game import Game as BaseGame

class Game(BaseGame):

    kickback_enabled = False
    magnets_enabled = False
    flippers_enabled = False
    loop_enabled = False
    playfield_enabled = False

    def kickback_enable(self):
        #if self.kickback_enabled:
        #    return
        p.coils["kickback"].auto_pulse(p.switches["kickback"])
        self.kickback_enabled = True

    def kickback_disable(self):
        #if not self.kickback_enabled:
        #    return
        p.coils["kickback"].auto_cancel()
        self.kickback_enabled = False

    def magnets_assist(self):
        #if self.magnets_enabled == "assist":
        #    return
        p.coils["magnet_left"].auto_patter(p.switches["magnet_left"], 1, 1)
        p.coils["magnet_center"].auto_patter(p.switches["magnet_center"], 1, 1)
        p.coils["magnet_right"].auto_patter(p.switches["magnet_right"], 1, 1)
        self.magnets_enabled = "assist"

    def magnets_disable(self):
        #if not self.magnets_enabled:
        #    return
        p.coils["magnet_left"].auto_cancel()
        p.coils["magnet_center"].auto_cancel()
        p.coils["magnet_right"].auto_cancel()
        self.magnets_enabled = False

    def flippers_enable(self):
        #if self.flippers_enabled:
        #    return
        p.flippers["left"].auto_pulse()
        p.flippers["right"].auto_pulse()
        self.flippers_enabled = True

    def loop_enable(self):
        #if self.loop_enabled:
        #    return
        p.flippers["right_up"].auto_pulse()
        self.loop_enabled = True

    def loop_disable(self):
        #if not self.loop_enabled:
        #    return
        p.flippers["right_up"].auto_cancel()
        self.loop_enabled = False

    def flippers_disable(self):
        #if not self.flippers_enabled:
        #    return
        self.loop_disable()
        p.flippers["left"].auto_cancel()
        p.flippers["right"].auto_cancel()
        self.flippers_enabled = False

    def playfield_enable(self):
        #if self.playfield_enabled:
        #    return
        p.coils["slingshot_left"].auto_pulse(p.switches["slingshot_left"])
        p.coils["slingshot_right"].auto_pulse(p.switches["slingshot_right"])
        self.flippers_enable()
        self.playfield_enabled = True

    def playfield_disable(self):
        #if not self.playfield_enabled:
        #    return
        p.coils["slingshot_left"].auto_cancel()
        p.coils["slingshot_right"].auto_cancel()
        self.kickback_disable()
        self.magnets_disable()
        self.flippers_disable()
        self.playfield_enabled = False

