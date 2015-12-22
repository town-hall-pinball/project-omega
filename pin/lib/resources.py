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
import json
import logging
import pygame
from pygame.locals import *
import struct

from pin.lib import p, dmd, util

fonts = {}
images = {}
sounds = {}
movies = {}
music = {}

log = logging.getLogger("pin.resources")
base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "resources")

class Music(object):

    def __init__(self, path, loop=False, start_time=0):
        self.path = path
        self.start_time = start_time
        self.loop = loop

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
        p.timers.cancel(self.timer)

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


class BitmapFont(object):

    def __init__(self, path):
        self.bitmap = load_dmd_animation(path)[0]
        metrics_file = re.sub(r"\.dmd$", ".metrics.json", path)
        with open(metrics_file) as fp:
            self.info = json.load(fp)

        self.info["left"] = self.info.get("left", 0)
        self.info["left_override"] = self.info.get("left_override", {})
        self.info["chars"] = self.info.get("chars", {})
        self.tracking = self.info.get("tracking", 2)

        self.widths = {}
        self.lefts = {}
        left = self.info["left"]
        self.char_size = self.bitmap.get_width() / 10
        for ch, width in self.info["widths"]:
            if width > 0:
                self.widths[ch] = width
                self.lefts[ch] = self.info["left_override"].get(ch, left)


    def metrics(self, text):
        result = []
        for char in text:
            if char not in self.widths:
                result += [(0, 0, 0, 0, 0)]
            else:
                result += [(0, self.widths[char], 0, self.char_size,
                        self.widths[char] + self.tracking)]
        return result

    def get_ascent(self):
        return self.char_size

    def render(self, text, antialias=True, color=None, background=None):
        width = 0
        metrics = self.metrics(text)
        width += reduce(lambda a, b: a + b[1], metrics, 0)
        width += reduce(lambda a, b: a + b[4], metrics[:-1], 0)
        frame = dmd.create_frame(width, self.char_size)

        xpos = 0
        for ch in text:
            xpos += self.render_char(frame, ch, xpos, color)
        return frame

    def render_char(self, frame, ch, xpos, color):
        if ch not in self.widths:
            return 0
        offset = ord(ch) - ord(' ')
        if offset < 0 or offset >= 96:
            offset = ord(' ')
        x = self.char_size * (offset % 10)
        y = self.char_size * (offset / 10)
        width = self.widths[ch]
        area = (x + self.lefts[ch], y, self.widths[ch], self.char_size)
        #print "char", ch, "area", area, "width", width

        if ch in self.info["chars"]:
            self.draw_char(frame, ch, xpos, width)
        else:
            frame.blit(self.bitmap, (xpos, 0), area=area)
        if color:
            actual = (0, 0, 0xff - color[2])
            frame.fill(actual, (xpos, 0, width, self.char_size),
                    special_flags=BLEND_SUB)
        return self.widths[ch] + self.tracking

    def draw_char(self, frame, ch, xpos, width):
        dots = dmd.create_dots(frame)
        data = self.info["chars"][ch]
        for y in xrange(self.char_size):
            for x in xrange(width):
                value = 0xff if data[y][x] == "*" else 0x0
                dots[xpos + x,y] = (value, value, value, value)


def load_fonts(*args):
    for arg in args:
        key = arg[0]
        filename = arg[1]
        size = arg[2] if len(arg) == 3 else None
        path = os.path.join(base_dir, filename)
        log.debug("Loading font {}: {}".format(key, filename))
        if filename.endswith(".dmd"):
            add("font", fonts, key, BitmapFont(path))
        else:
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

def available(path):
    path = os.path.join(base_dir, path)
    return os.path.exists(path)


