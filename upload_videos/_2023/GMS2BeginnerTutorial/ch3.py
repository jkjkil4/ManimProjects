from manimlib import *

class Intro(Scene):
    def construct(self) -> None:
        txt1 = Text('【GMS2】GameMaker Studio 2 零基础入门教程', color=GREY_D).scale(0.6)
        txt1[:6].set_fill(BLUE_D)
        txt2 = Text('第3节 第一步尝试', color=GREY).scale(0.7)
        txt = VGroup(txt1, txt2).arrange(DOWN).set_stroke(BLACK)

        self.wait(0.1)
        self.play(DrawBorderThenFill(txt))
        self.wait()
        self.play(FadeOut(txt))

class _1(Scene):
    
