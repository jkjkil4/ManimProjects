from manimlib import *

class Intro(Scene):
    def construct(self) -> None:
        txt1 = Text('【GMS2】GameMaker Studio 2 零基础入门教程', color=GREY_D).scale(0.6)
        txt1[:6].set_fill(BLUE_D)
        txt2 = Text('第1节 概况介绍', color=GREY).scale(0.7)
        txt = VGroup(txt1, txt2).arrange(DOWN).set_stroke(BLACK)

        self.wait(0.1)
        self.play(DrawBorderThenFill(txt))
        self.wait()
        self.play(FadeOut(txt))

class _1(Scene):
    def construct(self) -> None:
        txt1 = Text("GameMaker")
        txt2 = Text("游戏引擎")
        vg = VGroup(txt1, txt2).set_color(GREY_D).scale(0.7).arrange(DOWN)
        self.play(AnimationGroup(*map(Write, vg), lag_ratio=0.3))


        self.wait()

        self.play((txt1[1:4] + txt1[5:]).animate.set_color(GREY_B))

        self.wait()
        self.play(*map(Uncreate, vg))

class _2(Scene):
    def construct(self) -> None:
        ico = [
            ImageMobject(f'assets/gm/{name}.png').set_height(1)
            for name in ['GM8', 'GMS1', 'GMS2']
        ]
        title = [
            'GameMaker 8',
            'GameMaker Studio',
            'GameMaker Studio 2'
        ]
        desc = [
            '上一代 GM，由于 GM8 的破解版盛行，因此也是有一定用户群体的版本',
            'GMS，新代 GM 的旧版',
            'GMS2，目前持续维护的 GM 版本，和 GM8 一样有很多人用'
        ]

        ver = Group(*[
            Group(
                Group(a, Text(b).scale(0.7).set_color(GREY_D)).arrange(RIGHT),
                Text(c).scale(0.5).set_color('#666666')
            ).arrange(DOWN, aligned_edge=LEFT)
            for a, b, c in zip(ico, title, desc)
        ]).arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF).to_corner(UL)

        for one in ver:
            self.wait()
            self.play(
                AnimationGroup(
                    FadeIn(one[0], scale=0.8),
                    Write(one[1], run_time=1),
                    lag_ratio=0.15
                )
            )
        
        self.wait()
        self.play(
            FadeOut(ver[1], run_time=0.5),
            Group(ver[0], ver[2]).animate.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        )
        self.wait()

        gms2 = ver[2][0]
        self.play(
            FadeOut(Group(ver[0], ver[2][1]), run_time=0.5),
            gms2.animate.scale(0.9).move_to(ORIGIN)
        )
        self.wait()

        txt23 = Text('2.3+').set_color(GREY_D).scale(0.5).shift(DOWN * 0.8)
        self.play(Write(txt23))
        self.wait()
