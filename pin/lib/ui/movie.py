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
# FROM, OUT OF OR IN CONNECTION WITH TH

import pygame

from .. import p
from .component import Component

class Movie(Component):

    def __init__(self, movie=None, **style):
        style["movie"] = movie
        super(Movie, self).__init__(defaults={}, **style)
        self.has_alpha = False
        self.playing = False
        self.callback = None

    def auto_size(self):
        movie = p.movies[self.style["movie"]]
        movie_width, movie_height = movie.get_size()

        if self.width == None:
            self.width = movie_width
        if self.height == None:
            self.height = movie_height

    def start(self, callback=None):
        movie = p.movies[self.style["movie"]]
        self.layout()
        self.draw()
        movie.set_display(self.frame)
        movie.rewind()
        movie.play()
        self.playing = True
        self.invalidate()
        self.callback = callback

    def stop(self):
        if self.style["movie"]:
            movie = p.movies[self.style["movie"]]
            movie.stop()
            self.playing = False
            self.invalidate()

    def draw(self):
        if self.frame:
            return self.frame
        return super(Movie, self).draw()

    def on_render(self):
        if self.playing:
            self.invalidate()
            movie = p.movies[self.style["movie"]]
            if not movie.get_busy():
                self.playing = False
                if self.callback:
                    self.callback()
                    self.callback = None

    def __str__(self):
        return "movie({})".format(self.style["movie"])
