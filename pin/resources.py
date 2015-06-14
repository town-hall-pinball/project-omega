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

from pin import dmd, util

fonts = {}
images = {}
sounds = {}
music = {}

log = logging.getLogger("pin.resources")
base_dir = os.path.join(os.path.dirname(__file__), "..", "resources")

class Music(object):

    def __init__(self, path, start_time=0):
        self.path = path
        self.start_time = start_time


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
        add("image", images, key, load_dmd_animation(path)[0])

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
                    v = ord(str_frame[i])
                    new_dots[x, y] = (v, v, v, 0xff)
            frames.append(new_frame)
    return frames

def add(what, to, key, value):
    if key in to:
        raise ValueError("Duplicate {}: {}".format(what, key))
    to[key] = value

