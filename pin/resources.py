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

import os
import re
import logging
import pygame
import struct

import p
from pin import dmd, util

fonts = {}
images = {}
sounds = {}
movies = {}
music = {}

log = logging.getLogger("pin.resources")
base_dir = os.path.join(os.path.dirname(__file__), "..", "resources")

class Music(object):

    def __init__(self, path, start_time=0):
        self.path = path
        self.start_time = start_time


class Movie(object):

    def __init__(self, path):
        self.current = 0
        self.playing = False
        self.timer = None
        self.display = None
        self.frames = load_dmd_animation(path)

    def play(self):
        self.playing = True
        self.current = 0
        self.timer = p.timers.tick(self.render)

    def stop(self):
        self.playing = False
        p.timers.clear(self.timer)

    def rewind(self):
        self.current = 0

    def set_display(self, display):
        self.display = display

    def render(self):
        if not self.display:
            return
        self.display.blit(self.frames[self.current], (0, 0))
        self.current += 1
        if self.current >= len(self.frames):
            self.stop()

    def get_busy(self):
        return self.playing

    def get_size(self):
        return (p.dmd.width, p.dmd.height)


def load_fonts(*args):
    for key, filename, size in args:
        path = os.path.join(base_dir, filename)
        log.debug("Loading font {}: {}".format(key, filename))
        add("font", fonts, key, pygame.font.Font(path, size))

def alias_fonts(*args):
    for source, target in args:
        log.debug("Aliasing font {} to {}".format(source, target))
        add("font", fonts, target, fonts[source])

def load_images(*args):
    for key, filename in args:
        path = os.path.join(base_dir, filename)
        log.debug("Loading image {}: {}".format(key, filename))
        if filename.endswith(".dmd"):
            add("image", images, key, load_dmd_animation(path)[0])
        else:
            add("image", images, key, load_image(path))

def load_sounds(*args):
    for key, filename in args:
        path = os.path.join(base_dir, filename)
        log.debug("Loading sound {}: {}".format(key, filename))
        add("sound", sounds, key, pygame.mixer.Sound(path))

def register_music(*args):
    for arg in args:
        key = arg[0]
        filename = arg[1]
        options = arg[2] if len(arg) == 3 else {}
        path = os.path.join(base_dir, filename)
        log.debug("Registering music {}: {}".format(key, filename))
        add("music", music, key, Music(path, **options))

def register_movies(*args):
    for key, filename in args:
        path = os.path.join(base_dir, filename)
        log.debug("Registering movie {}: {}".format(key, filename))
        if filename.endswith(".dmd"):
            add("movie", movies, key, Movie(path))
        else:
            add("movie", movies, key, pygame.movie.Movie(path))


def load_dmd_animation(path):
    frames = []
    # Derived from
    # https://github.com/preble/pyprocgame/blob/master/procgame/dmd/animation.py
    with open(path) as f:
        f.seek(0, os.SEEK_END) # Go to the end of the file to get its length
        file_length = f.tell()
        f.seek(4) # Skip over the 4 byte DMD header.
        frame_count = struct.unpack("I", f.read(4))[0]
        width = struct.unpack("I", f.read(4))[0]
        height = struct.unpack("I", f.read(4))[0]
        if file_length != 16 + width * height * frame_count:
            raise ValueError("Corrupt DMD file")
        for frame_index in range(frame_count):
            str_frame = f.read(width * height)
            new_frame = dmd.create_frame(width, height)
            new_dots = dmd.create_dots(new_frame)
            for x in xrange(width):
                for y in xrange(height):
                    i = (y * width) + x
                    v = ord(str_frame[i]) * 16
                    if v > 0xff:
                        v = v & 0xff
                    new_dots[x, y] = (v, v, v, 0xff)
            frames.append(new_frame)
    return frames

def load_image(path):
    image = pygame.image.load(path)
    dots = dmd.create_dots(image)
    for x in xrange(image.get_width()):
        for y in xrange(image.get_height()):
            v = dots[x, y]
            nv = (v & 0xff000000) >> 24
            dots[x, y] = (nv, nv, nv, 0xff)
    return image


def add(what, to, key, value):
    if key in to:
        raise ValueError("Duplicate {}: {}".format(what, key))
    to[key] = value

def reset():
    fonts.clear()
    images.clear()
    sounds.clear()
    movies.clear()
    music.clear()



