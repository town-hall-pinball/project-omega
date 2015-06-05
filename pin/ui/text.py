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

import p
from .component import Component

class Text(Component):

    def __init__(self, text="", **style):
        style["text"] = text
        super(Text, self).__init__(defaults={
            "font": "title",
            "reverse": False,
            "color": 0xf,
            "x_align": "left",
        }, **style)
        self.area = None

    def show(self, text):
        self.style["text"] = text if text is not None else ""
        self.enable()

    def auto_size(self):
        font = p.fonts[self.style["font"]]
        metrics = font.metrics(self.style["text"])

        # Crop as tight as possible and only go below the baseline if
        # necessary
        text_height = max([x[3] - x[2] for x in metrics])
        descent = min(x[2] for x in metrics) * -1
        text_height += descent

        # Remove the advance on the last character
        text_width = sum([x[4] for x in metrics])
        text_width -= metrics[-1][4] - metrics[-1][1] - metrics[-1][0]

        if self.width == None:
            self.width = text_width
        if self.height == None:
            self.height = text_height

        self.area = (0, font.get_ascent() - self.height + descent, self.width,
                self.height)

    def draw(self):
        super(Text, self).draw()
        font = p.fonts[self.style["font"]]
        x = self.x
        y = self.y
        if self.style["x_align"] == "center":
            x += round((self.width / 2.0) - (text_width / 2.0))
        color = (0, 0, self.style["color"])
        text = font.render(self.style["text"], False, color)
        self.frame.blit(text, (0, 0), self.area)


