from . import test
from ..resources import load_font as font
from ..resources import load_image as image

def init():
    font("title",   "fonts/pf_arma_five.ttf", 8)
    font("title12", "fonts/pf_arma_five.ttf", 16)

    image("thp_logo", "images/thp_logo.dmd")

    test.start()


