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

import p
from pin.handler import Handler
from pin import ui, util


class Mode(Handler):

    def setup(self):
        self.sample = ".,1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.fonts = util.Cycle(sorted(p.fonts.keys()))
        self.display = ui.Panel(name="font_viewer")
        self.label = ui.Text(top=0, right=0, font="r7", padding=[1, 1])
        self.text = ui.Text(self.sample)
        self.display.add([self.label, self.text])

        self.on("switch_service_enter", self.start)
        self.on("switch_service_up", self.next)
        self.on("switch_service_down", self.previous)
        self.on("switch_service_exit",  self.exit)
        self.on("switch_flipper_left", self.flipper_left_down)
        self.on("switch_flipper_right", self.flipper_right_down)
        self.on("switch_flipper_left_inactive", self.flipper_up)
        self.on("switch_flipper_right_inactive", self.flipper_up)

        self.timer = None
        self.scroll_left = util.Show("scroll_left", [0.05],
                repeat=True, action=self.text_left)
        self.scroll_right = util.Show("scroll_right", [0.05],
                repeat=True, action=self.text_right)

    def on_enable(self):
        self.start()

    def start(self):
        self.update()

    def next(self):
        p.mixer.play("service_select")
        self.fonts.next()
        self.start()

    def previous(self):
        p.mixer.play("service_select")
        self.fonts.previous()
        self.start()

    def update(self):
        key = self.fonts.get()
        self.label.show(key)
        self.text.update(font=key)

    def flipper_left_down(self):
        self.text_left()
        self.timer = self.wait(0.2, self.scroll_left.start)

    def flipper_right_down(self):
        self.text_left()
        self.timer = self.wait(0.2, self.scroll_right.start)

    def flipper_up(self):
        self.cancel(self.timer)
        self.scroll_left.stop()
        self.scroll_right.stop()

    def text_left(self):
        self.sample = self.sample[1:] + self.sample[0]
        self.text.show(self.sample)

    def text_right(self):
         self.sample = self.sample[-1:] + self.sample[:-1]
         self.text.show(self.sample)

    def on_disable(self):
        p.mixer.play("service_exit")
        p.modes["service"].resume()
        self.scroll_left.stop()
        self.scroll_right.stop()

    def exit(self):
        self.disable()
