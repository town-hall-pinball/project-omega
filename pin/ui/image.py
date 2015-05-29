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
# FROM, OUT OF OR IN CONNECTION WITH TH

import pin
from .component import Component

class Image(Component):

    def __init__(self, **style):
        super(Image, self).__init__(defaults={
            "image": None,
            "reverse": False
        }, **style)

    def auto_size(self):
        if self.style["image"] != None:
            image =  pin.images[self.style["image"]]
            width = image.get_width()
            height = image.get_height()
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
        image = pin.images[self.style["image"]]
        self.frame.blit(image, (0, 0))