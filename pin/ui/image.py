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
from .component import Component

class Image(Component):

    def __init__(self, image=None, **style):
        style["image"] = image
        super(Image, self).__init__(defaults={
            "reverse": False
        }, **style)
        self.reverse = None

    def auto_size(self):
        if self.style["image"] != None:
            image =  p.images[self.style["image"]]
            width = (image.get_width() + self.style["padding_left"] +
                    self.style["padding_right"])
            height = (image.get_height() + self.style["padding_top"] +
                    self.style["padding_bottom"])
        else:
            width = 0
            height = 0
        if self.width == None:
            self.width = width
        if self.height == None:
            self.height = height

    def draw(self):
        super(Image, self).draw()
        if self.width == 0 or self.height == 0:
            return
        image = p.images[self.style["image"]]
        if self.style["reverse"] and not self.reverse:
            image = image.copy()
            dots = p.dmd.create_dots(image)
            for x in xrange(image.get_width()):
                for y in xrange(image.get_height()):
                    dots[x, y] = (dots[x, y]) ^ 0x00ffffff
            del dots
        self.frame.blit(image, (self.style["padding_left"],
                self.style["padding_top"]))

    def __str__(self):
        name = self.style.get("image", None)
        return "image({})".format(name) if name else "image"
