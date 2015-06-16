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
        self.movies = util.Cycle(p.movies.items())
        self.panel = ui.Panel()
        self.player = ui.Movie()
        self.label = ui.Text(top=0, right=0)
        self.panel.add([self.player, self.label])

        self.on("switch_service_exit",  self.exit)

    def enabled(self):
        p.dmd.stack("movie_browser", self.panel)
        self.update()

    def update(self):
        key, movie = self.movies.get()
        self.player.stop()
        self.player.update(movie=key)
        self.player.start()
        self.label.show(key)

    def disabled(self):
        p.mixer.play("service_exit")
        p.dmd.remove("movie_browser")
        p.modes["service"].resume()

    def exit(self):
        self.disable()

