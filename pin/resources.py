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

from pin import dmd

__all__ = ["fonts", "images", "font", "image"]

fonts = {}
images = {}

log = logging.getLogger("pin.resources")
base_dir = os.path.join(os.path.dirname(__file__), "..", "resources")

pygame.font.init()

def load_fonts(*args):
    for key, filename, size in args:
        path = os.path.join(base_dir, filename)
        log.debug("Loading font {}: {}".format(key, filename))
        fonts[key] = pygame.font.Font(path, size)

def load_images(*args):
    for key, filename in args:
        path = os.path.join(base_dir, filename)
        log.debug("Loading image {}: {}".format(key, filename))
        images[key] = load_dmd_animation(path)[0]

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
                    new_dots[x, y] = ord(str_frame[i])
            frames.append(new_frame)
    return frames



