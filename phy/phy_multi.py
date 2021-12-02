import sys
sys.path.append('.')
from header import *
from phy.phy_header import *
from manimlib import *

class TestScene(Scene):
    def construct(self):
        arrow = PhyArrowEquip('', grad_up_step = 1, grad_down = False).scale(2)
        self.add(arrow)

