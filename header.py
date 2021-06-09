import sys
sys.path.append("manim")
from manimlib import *

def eqRange(fromValue, toValue, step = 1):
    value = fromValue
    while(value <= toValue):
        yield value
        value += step