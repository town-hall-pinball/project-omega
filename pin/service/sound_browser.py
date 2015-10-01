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

from ..lib.handler import Handler
from ..lib import p, ui, util

class Mode(Handler):

    def setup(self):
        self.sounds = util.Cycle(sorted(p.sounds.keys()))
        self.display = ui.Panel(name="sound_player")
        self.label = ui.Text(case="full")
        self.display.add([self.label])

        self.on("switch_service_enter", self.update)
        self.on("switch_service_up", self.next)
        self.on("switch_service_down", self.previous)
        self.on("switch_service_exit",  self.exit)

    def on_enable(self):
        self.play()

    def play(self):
        self.update()

    def next(self):
        self.sounds.next()
        self.play()

    def previous(self):
        self.sounds.previous()
        self.play()

    def update(self):
        key = self.sounds.get()
        p.mixer.play(key)
        self.label.show(key)

    def on_disable(self):
        p.mixer.stop()
        p.mixer.play("service_exit")
        p.modes["service"].resume()

    def exit(self):
        self.disable()

    def select(self, sound):
        self.sounds.select(sound)
        self.update()

