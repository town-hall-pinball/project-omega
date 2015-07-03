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

    font_case = {
        "title": "G",
        "number": ",",
        "full": "g,",
    }

    def __init__(self, text="", **style):
        style["text"] = text
        super(Text, self).__init__(defaults={
            "font": "title",
            "reverse": False,
            "color": 0xf,
            "x_align": "left",
            "case": "full"
        }, **style)
        self.area = None

    def show(self, text, duration=None):
        self.style["text"] = text if text is not None else ""
        super(Text, self).show(duration)
        self.auto_size()
        self.invalidate()

    def auto_size(self):
        font = p.fonts[self.style["font"]]
        width_metrics = font.metrics(self.style["text"])
        height_metrics = font.metrics(self.font_case[self.style["case"]])

        if not width_metrics:
            self.height = 0
            self.width = 0
            self.area = (0, 0, 0, 0)
            return

        # Crop as tight as possible and only go below the baseline if
        # necessary
        text_height = max([x[3] - x[2] for x in height_metrics])
        self.descent = min(x[2] for x in height_metrics) * - 1
        text_height += self.descent

        # Remove the advance on the last character
        text_width = sum([x[4] for x in width_metrics])
        text_width -= (width_metrics[-1][4] - width_metrics[-1][1] -
                width_metrics[-1][0])

        if self.width == None:
            self.width = (text_width + self.style["padding_left"] +
                    self.style["padding_right"])
        if self.height == None:
            self.height = (text_height + self.style["padding_top"] +
                    self.style["padding_bottom"])

        self.area = (0, font.get_ascent() - self.height + self.descent,
                self.width, self.height)

    def draw(self):
        super(Text, self).draw()
        font = p.fonts[self.style["font"]]
        x = self.x
        y = self.y
        offset_x = self.style["padding_left"]
        offset_y = self.style["padding_top"]
        if self.style["x_align"] == "center":
            x += round((self.width / 2.0) - (text_width / 2.0))
        color = (0, 0, self.style["color"] * 16)
        text = font.render(self.style["text"], False, color)
        self.frame.blit(text, (offset_x, -offset_y), self.area)

    def __str__(self):
        return "text({})".format(self.style["text"])

