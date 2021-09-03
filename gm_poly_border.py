import sys
sys.path.append(".")
import header as h
from manimlib import *

class PBOpeningScene(h.OpeningScene):
    str1 = "多边形框——限制、遮罩与叠加"
    str2 = "算法分享"
    style = 1
    img_time = 1.3
    txt1_time = 1.5

class Show(Scene):
    def construct(self):
        self.add(h.txtwatermark())
        h.chapter_animate(self, "Ⅰ", "效果展示", GREY_A)
        
        