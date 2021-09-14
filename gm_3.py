import sys
sys.path.append(".")
import header as h
from manimlib import *

txtColor = "#333333"
txtColor2 = "#555555"

class GMOpeningScene(h.OpeningScene):
    str1 = "GameMaker 教程"
    str2 = "基本事件"

class GMTimeScene(h.TimeScene):
    info_list = [
        ["00:12", "步事件"]
    ]

class StepEvent(Scene):
    def construct(self):
        self.add(h.watermark())

        rect = Rectangle(
            (FRAME_X_RADIUS - DEFAULT_MOBJECT_TO_EDGE_BUFFER) * 2, 
            (FRAME_Y_RADIUS - DEFAULT_MOBJECT_TO_EDGE_BUFFER) * 2,
            color = BLUE
            )
        self.play(FadeIn(rect))
        self.wait()
        self.play(FadeOut(rect, UP))
