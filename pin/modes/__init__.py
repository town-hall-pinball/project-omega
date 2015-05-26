from . import test
from ..resources import load_font as font

def init():
    font("title", "fonts/pf_arma_five.ttf", 8)
    test.start()


