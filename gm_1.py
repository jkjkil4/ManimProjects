import sys
sys.path.append(".")
import header as h
from manimlib import *

'''
简介的内容:
GM8: https://down.magecorn.com/s/gm8
GMS2 Steam: https://store.steampowered.com/app/585410/GameMaker_Studio_2_Desktop/
'''

txtColor = "#333333"
txtColor2 = "#555555"

class GMOpeningScene(h.OpeningScene):
    str1 = "GameMaker 教程"
    str2 = "基本介绍"

class GMTimeScene(h.TimeScene):
    info_list = [
        ["00:12", "简要概述"],
        ["00:36", "关于GMS2"],
        ["01:07", "DnD 和 GML"],
        ["01:32", "杂谈"]
    ]
    
class AboutGM(Scene):
    def construct(self):
        self.add(h.watermark())

        txt1 = Text("GameMaker 是一个游戏制作引擎", color = txtColor).shift(UP * 3)
        self.play(DrawBorderThenFill(txt1))
        self.wait(0.6)
        txt2 = Text("其主要可以分为3大版本", color = txtColor2).next_to(txt1, DOWN)
        txt3 = Text("按时间顺序排列为", color = txtColor2).next_to(txt1, DOWN)
        self.play(Write(txt2))
        self.wait()
        self.play(Transform(txt2, txt3))
        self.wait()

        imgGM8 = ImageMobject("assets/gm/GM8.png", height = 1).shift(LEFT * 3.5 + UP)
        txtGM8 = Text("GameMaker 8", color = txtColor2).next_to(imgGM8, DOWN)
        groupGM8 = Group(imgGM8, txtGM8)
        self.play(FadeIn(groupGM8))

        imgGMS = ImageMobject("assets/gm/GMS1.png", height = 1).shift(UP)
        txtGMS = Group(
            Text("GameMaker", color = txtColor2),
            Text("Studio", color = txtColor2)
            ).arrange(DOWN).next_to(imgGMS, DOWN)
        groupGMS = Group(imgGMS, txtGMS)
        self.play(FadeIn(groupGMS))

        imgGMS2 = ImageMobject("assets/gm/GMS2.png", height = 1).shift(RIGHT * 3.5 + UP)
        txtGMS2 = Group(
            Text("GameMaker", color = txtColor2),
            Text("Studio 2", color = txtColor2)
            ).arrange(DOWN).next_to(imgGMS2, DOWN)
        groupGMS2 = Group(imgGMS2, txtGMS2)
        self.play(FadeIn(groupGMS2))
        self.wait()

        txtMore = Text("目前用得最多的是 GM8 和 GMS2", color = txtColor).shift(DOWN * 1.5)
        self.play(DrawBorderThenFill(txtMore), groupGMS.animate.set_opacity(0.2))
        self.wait()

        txtAboutGMS2 = Text("GMS2 是目前的最新版，你可以在 Steam 或者 yoyogames官网 购买", color = txtColor).next_to(txtMore, DOWN)
        self.play(Write(txtAboutGMS2), run_time = 3)
        self.wait()

        txtAboutGM8 = Text("GM8 虽然版本较老，但是由于新版在某些方面的门槛，仍有不少人使用该版本", color = txtColor).next_to(txtAboutGMS2, DOWN)
        self.play(Write(txtAboutGM8), run_time = 3.2)
        
        txtLink = Text("*相关链接可以在简介中找到", color = txtColor2).scale(0.5).next_to(txtAboutGM8, DOWN)
        self.play(DrawBorderThenFill(txtLink))
        self.wait(2)

        self.play(
            FadeOut(txt1), FadeOut(txt2), FadeOut(groupGM8), FadeOut(groupGMS), 
            FadeOut(txtMore), FadeOut(txtAboutGMS2), FadeOut(txtAboutGM8), FadeOut(txtLink),
            groupGMS2.animate.to_edge(UL)
            )
        
        txtBlock = Text("GMS2的门槛和缺点 相对于GM8来说是什么?", color = txtColor)\
            .next_to(groupGMS2, buff = LARGE_BUFF, aligned_edge = UP).shift(DOWN * 0.2)
        self.play(DrawBorderThenFill(txtBlock))
        self.wait()

        txtBlock1 = VGroup(
            Text("-", color = txtColor2),
            Text("购买GMS2需要花钱", color = txtColor)
            ).arrange().scale(0.9).next_to(txtBlock, DOWN, LARGE_BUFF, LEFT)
        imgBlock1 = ImageMobject("assets/gm/gms2_in_steam.png").set_height(1).next_to(txtBlock1, DOWN, aligned_edge = LEFT).shift(RIGHT * 0.5)
        self.play(FadeIn(txtBlock1, scale_factor = 0.7), FadeIn(imgBlock1))
        self.wait(1.6)
        self.play(FadeOut(imgBlock1), run_time = 0.4)

        txtBlock2 = VGroup(
            Text("-", color = txtColor2),
            Text("GMS2有对国内来说十分麻烦的注册步骤（指科学上网）", color = txtColor)
            ).arrange().scale(0.9).next_to(txtBlock1, DOWN, aligned_edge = LEFT)
        imgBlock2 = ImageMobject("assets/404.png").set_height(1).next_to(txtBlock2, DOWN, aligned_edge = LEFT).shift(RIGHT * 0.5)
        self.play(FadeIn(txtBlock2, scale_factor = 0.7), FadeIn(imgBlock2))
        self.wait(1.6)
        self.play(FadeOut(imgBlock2), run_time = 0.4)

        txtBlock3 = VGroup(
            Text("-", color = txtColor2),
            Text("GMS2每次使用都要联网验证", color = txtColor)
            ).arrange().scale(0.9).next_to(txtBlock2, DOWN, aligned_edge = LEFT)
        self.play(FadeIn(txtBlock3, scale_factor = 0.7))

        txtBlock4 = Text("...", color = txtColor2).scale(0.9).next_to(txtBlock3, DOWN, aligned_edge = LEFT)
        self.play(FadeIn(txtBlock4), run_time = 0.5)
        self.wait(1.6)
        
        txtNBlock1 = Text("虽然有不少人使用GM8", color = txtColor2)\
            .scale(0.9).next_to(txtBlock4, DOWN, LARGE_BUFF, LEFT)
        self.play(Write(txtNBlock1))
        self.wait(0.8)

        txtNBlock2 = Text("但是如果上述或更多问题能够解决的话，最好还是用GMS2", color = txtColor2)\
            .scale(0.9).next_to(txtNBlock1, DOWN, aligned_edge = LEFT)
        self.play(Write(txtNBlock2), run_time = 2)
        self.wait(0.8)

        txtNBlock3 = Text("并且GMS2也有更多易用的功能", color = txtColor2)\
            .scale(0.9).next_to(txtNBlock2, DOWN, aligned_edge = LEFT)
        self.play(Write(txtNBlock3), run_time = 1.7)
        self.wait(0.4)

        txtNBlock4 = Text("*貌似可以无限期试用", color = txtColor2)\
            .scale(0.5).next_to(txtNBlock3, DOWN, aligned_edge = LEFT)
        self.play(DrawBorderThenFill(txtNBlock4))
        self.wait()

        self.play(
            FadeOut(groupGMS2),
            FadeOut(txtBlock), FadeOut(txtBlock1), FadeOut(txtBlock2), FadeOut(txtBlock3), FadeOut(txtBlock4),
            FadeOut(txtNBlock1), FadeOut(txtNBlock2), FadeOut(txtNBlock3), FadeOut(txtNBlock4)
            )
        
        txtDo1 = Text("本教程将会以GMS2为基础进行讲解", color = txtColor).shift(UP * 0.5)
        self.play(Write(txtDo1))
        self.wait()

        txtDo2 = Text("但同时也会在一定程度上对和GM8有差别的部分进行说明", color = txtColor)
        self.play(Write(txtDo2), run_time = 2.3)
        self.wait(2)

        self.play(FadeOut(txtDo1), FadeOut(txtDo2))

class DnD_And_GML(Scene):
    def construct(self):
        self.add(h.watermark())

        txt1 = Text("在GameMaker中，编辑方式分为", color = txtColor).to_edge(UL)
        txt2 = VGroup(
            Text("DnD", color = GREEN), Text("（Drag and Drop）", color = txtColor),
            Text("和", color = txtColor), 
            Text("GML", color = GREEN), Text("（GameMaker Language）", color = txtColor)
            ).arrange().next_to(txt1, DOWN, aligned_edge = LEFT)
        img1 = ImageMobject("assets/gm/DnD_and_GML.png", height = 1).to_edge(UR)
        self.play(Write(txt1), run_time = 0.8)
        self.play(Write(txt2), FadeIn(img1))
        self.wait(1.5)

        txtDnD = VGroup(Text("DnD", color = GREEN), Text("是一种拖放功能块的便捷编辑方式", color = txtColor, t2c = { "拖放功能块": ORANGE }))\
            .arrange().next_to(txt2, DOWN, MED_LARGE_BUFF, LEFT)
        imgDnD = ImageMobject("assets/gm/DnD.png", height = 2.4).next_to(txtDnD, DOWN)
        self.play(Write(txtDnD), FadeIn(imgDnD))
        self.wait()

        txtGML = VGroup(Text("GML", color = GREEN), Text("是一种使用代码的编辑方式", color = txtColor, t2c = { "使用代码": ORANGE }))\
            .arrange().next_to(txtDnD, buff = LARGE_BUFF)
        imgGML = ImageMobject("assets/gm/GML.png", height = 2.4).next_to(txtGML, DOWN)
        self.play(Write(txtGML), FadeIn(imgGML))
        self.wait()

        txtN1 = VGroup(Text("虽然", color = txtColor2), Text("DnD", color = GREEN), Text("更加直观", color = txtColor2))\
            .arrange().scale(0.9).next_to(imgDnD, DOWN, MED_LARGE_BUFF, LEFT).shift(LEFT * 0.5)
        self.play(Write(txtN1))
        self.wait()

        txtN2 = VGroup(
            Text("但是随着学习的深入，", color = txtColor2), Text("DnD", color = GREEN), 
            Text("的局限性会越发凸显", color = txtColor2, t2c = { "局限性": RED })
            ).arrange().scale(0.9).next_to(txtN1, DOWN, aligned_edge = LEFT)
        self.play(Write(txtN2))
        self.wait()
        
        txtN3 = VGroup(
            Text("所以建议学习", color = txtColor2), Text("GML", color = GREEN), 
            Text("而不是", color = txtColor2), Text("DnD", color = GREEN)
            ).arrange().scale(0.9).next_to(txtN2, DOWN, aligned_edge = LEFT)
        self.play(Write(txtN3))
        self.play(txtDnD.animate.set_opacity(0.4), imgDnD.animate.set_opacity(0.4))
        self.wait()
        
        txtN4 = VGroup(Text("本教程也将会使用", color = txtColor2), Text("GML", color = GREEN), Text("进行讲解", color = txtColor2))\
            .arrange().scale(0.9).next_to(txtN3, DOWN, aligned_edge = LEFT)
        self.play(Write(txtN4))
        self.wait(2)

        self.play(
            *[FadeOut(img) for img in [img1, imgDnD, imgGML]], 
            *[Uncreate(mobj) for mobj in [txt1, txt2, txtDnD, txtGML, txtN1, txtN2, txtN3, txtN4]],
            run_time = 1.2)

class Talk(Scene):
    def construct(self):
        self.add(h.watermark())

        txtTalk1 = Text("有人可能会说写代码（编程）的学习成本更高", color = txtColor).to_edge(UL, LARGE_BUFF)
        self.play(Write(txtTalk1))
        self.wait()

        txtTalk2 = Text("当然，编程确实更难", color = txtColor)\
            .next_to(txtTalk1, DOWN, aligned_edge = LEFT)
        self.play(Write(txtTalk2))
        self.wait()

        txtTalk3 = Text("但是，当你学会编程后，实现功能时可以更加灵活", color = txtColor, t2c = { "灵活": ORANGE })\
            .next_to(txtTalk2, DOWN, aligned_edge = LEFT)
        self.play(Write(txtTalk3))
        self.wait()

        txtTalk4 = Text("不要没学就开始打退堂鼓", color = txtColor).next_to(txtTalk3, DOWN, aligned_edge = LEFT).insert_n_curves(50)
        self.play(Write(txtTalk4))
        self.wait()

        txtTalk5 = Text("关键在于你愿不愿意学、想不想学", color = txtColor).next_to(txtTalk4, DOWN, aligned_edge = LEFT)
        self.play(Write(txtTalk5))
        self.wait(2)

        self.play(*[FadeOut(mobj) for mobj in [txtTalk1, txtTalk2, txtTalk3, txtTalk4, txtTalk5]])
        
class GMEndScene(h.EndScene):
    strBgm = "Staff Roll - Triodust"