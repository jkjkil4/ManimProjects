import sys
sys.path.append('.')
from phy.phy_header import *
from header import *

class PhyRefitOpeningScene(Scene):
    def construct(self):
        self.add(txtwatermark())
        self.wait(0.5)

        phyG = LinedPhyEquip(PhyEquipTxt("G").scale(0.8)).scale(0.6)
        phyG.phyEquip.txt.insert_n_curves(8)
        phyA = LinedPhyEquip(PhyEquipTxt("A").scale(0.8)).scale(0.6)
        phyV = LinedPhyEquip(PhyEquipTxt("V").scale(0.8)).scale(0.6)
        phyGroup = Group(phyG, phyA, phyV).arrange(buff = LARGE_BUFF).to_edge(UP, LARGE_BUFF * 2)
        
        phyGTxt = Text("灵敏电流计", color = BLUE).scale(0.6).next_to(phyG.phyEquip, UR, SMALL_BUFF)
        phyATxt = Text("电流表", color = BLUE).scale(0.6).next_to(phyA.phyEquip, UR, SMALL_BUFF)
        phyVTxt = Text("电压表", color = BLUE).scale(0.6).next_to(phyV.phyEquip, UR, SMALL_BUFF)

        phyGArrow = Arrow(phyG.phyEquip.get_bottom(), phyG.phyEquip.get_bottom() + DOWN).set_color(BLUE)
        phyAArrow = Arrow(phyA.phyEquip.get_bottom(), phyA.phyEquip.get_bottom() + DOWN).set_color(BLUE)
        phyVArrow = Arrow(phyV.phyEquip.get_bottom(), phyV.phyEquip.get_bottom() + DOWN).set_color(BLUE)

        phyGTex = Tex("R\\rightarrow0").next_to(phyGArrow, DOWN)
        phyATex = Tex("R\\rightarrow0").next_to(phyAArrow, DOWN)
        phyVTex = Tex("R\\rightarrow+\\infty").next_to(phyVArrow, DOWN)
        
        txt1 = Text("我们在初中所接触到的电表", t2c = { "电表": BLUE }).scale(0.9)
        txt2 = Text("一般是理想电表", t2c = { "理想": GOLD, "电表": BLUE }).scale(0.9)
        Group(txt1, txt2).arrange(DOWN).to_edge(DOWN)
        
        self.play(FadeIn(phyG, UP), run_time = 0.8)
        self.play(FadeIn(phyA, UP), Write(txt1), run_time = 0.8)
        self.play(FadeIn(phyV, UP), Write(txt2), run_time = 0.8)
        self.play(*[FadeIn(m, UR / 2) for m in [phyGTxt, phyATxt, phyVTxt]])
        self.play(*[GrowArrow(m) for m in [phyGArrow, phyAArrow, phyVArrow]])
        self.play(*[FadeTransform(txt2[3:5].copy(), tex) for tex in [phyGTex, phyATex, phyVTex]])
        self.wait(0.5)
        self.play(phyGroup.animate.set_opacity(0.2))

        lineG = Line(phyG.get_left(), phyG.get_right(), width = 3)
        lineA = Line(phyA.get_left(), phyA.get_right(), width = 3)
        lineV = VGroup(
            Line(phyV.lineLeft.get_left(), phyV.lineLeft.get_right() + RIGHT * 0.1),
            Line(phyV.lineRight.get_left() + LEFT * 0.1, phyV.lineRight.get_right()),
            Text("x", color = RED).scale(1.5).move_to(phyV)
            )
        self.play(GrowArrow(lineG), GrowArrow(lineA), Write(lineV))
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in [lineG, lineA, lineV]], phyGroup.animate.set_opacity(1))
        self.wait()

        txt3 = Text("之后我们便知道，在现实中电表的电阻不是理想的", t2c = { "电表": BLUE, "不是理想的": GOLD }).scale(0.8)
        txt4 = Text("并且，常见的电表由表头改装而来", t2c = { "表头": BLUE }).scale(0.8)
        Group(txt3, txt4).arrange(DOWN).to_edge(DOWN)
        crosses = [Cross(tex).insert_n_curves(8) for tex in [phyGTex, phyATex, phyVTex]]
        self.play(Write(txt3), *[FadeOut(m, run_time = 0.5) for m in [txt1, txt2]])
        self.play(*[ShowCreation(cross) for cross in crosses])
        self.wait(0.8)
        self.play(
            Group(phyG, phyGTxt).animate.move_to(ORIGIN), Write(txt4),
            *[FadeOut(m) for m in [phyA, phyV, phyATxt, phyVTxt, phyGArrow, phyAArrow, phyVArrow, phyGTex, phyATex, phyVTex, *crosses]]
            )
        self.play(Transform(phyGTxt, Text("表头", color = BLUE).scale(0.6).next_to(phyG.phyEquip, UR, SMALL_BUFF)))
        self.wait()
        self.play(*[FadeOut(m) for m in [phyG, phyGTxt, txt3, txt4]], run_time = 0.6)

class PhyRefitTitleScene(Scene):
    def construct(self):
        self.add(txtwatermark())
        txt = Text("【物理】电表的改装与校准", t2c = { "【物理】": BLUE }).scale(1.4)
        self.play(DrawBorderThenFill(txt))
        self.wait()
        self.play(FadeOut(txt))

class PhyRefitG2AScene(Scene):
    def construct(self):
        self.add(txtwatermark())

        phyG = PhyEquipTxt("G").scale(0.5)
        phyG.txt.insert_n_curves(8)
        self.play(FadeIn(phyG))

        txt1 = Text("表头的量程相当的小", t2c = { "表头": BLUE }).scale(0.8)
        txt2 = Text("可以通过改装将其变为常用的量程相对较大的电流表和电压表", t2c = { "改装": GOLD, "电流表": BLUE, "电压表": BLUE }).scale(0.8)
        Group(txt1, txt2).arrange(DOWN).to_edge(DOWN)
        self.play(Write(txt1))
        self.play(Write(txt2))
        self.wait()

        txt3 = Text("在这之前，我们要知道表头的几个基本属性", t2c = { "基本属性": BLUE }).scale(0.8).to_corner(DOWN)
        self.play(FadeOut(txt1, run_time = 0.3), FadeOut(txt2, run_time = 0.3), Write(txt3))

        phyArwG = PhyArrowEquip(grad_up_range = (0, 0), grad_up_step = 0, grad_cnt = 3)\
            .scale(2).next_to(BOTTOM, UP, buff = -1.2)
        srdrectArwG = SurroundingRectangle(phyArwG).set_color(WHITE)
        texIg = Tex("I_{g}", color = RED)
        vgRg = VGroup(Tex("R_{g}", color = GREEN), Text("表头的内阻")).arrange().scale(0.8)
        vgIg = VGroup(texIg.copy(), Text("表头的满偏电流")).arrange().scale(0.8)
        texMul = Tex("I_{g} \\cdot R_{g}")
        texMul[0][:2].set_color(RED)
        texMul[0][3:5].set_color(GREEN)
        vgUg = VGroup(Tex("U_{g}", color = YELLOW), Text("表头的满偏电压").insert_n_curves(8), texMul).arrange().scale(0.8)
        vgRels = VGroup(vgRg, vgIg, vgUg).arrange(DOWN, aligned_edge = LEFT).next_to(phyG.get_right() + LEFT * 2)
        self.play(phyG.animate.shift(LEFT * 2), *[FadeIn(m[0], RIGHT) for m in vgRels])
        self.play(Write(vgRg[1:]))
        self.wait(0.5)
        self.play(Write(vgIg[1:]))
        self.play(FadeOut(txt3, DOWN), FadeIn(phyArwG, UP), FadeIn(srdrectArwG, UP))
        self.play(phyArwG.arrow_offset.animate.set_value(30))
        texIg.next_to(phyArwG.arrow, UR, SMALL_BUFF)
        self.play(DrawBorderThenFill(texIg), run_time = 0.5)
        self.wait(0.5)
        self.play(Transform(texIg, vgIg[0]))
        self.remove(texIg)
        self.play(FadeOut(phyArwG, DOWN), FadeOut(srdrectArwG, DOWN))
        self.wait(0.5)
        self.play(Write(vgUg[1:]))
        self.wait(0.5)
        self.play(ShowCreationThenFadeAround(vgRels))
        self.wait(0.5)
        self.play(FadeOut(vgRels))
        
        txtG2A = VGroup(
            VGroup(PhyEquipTxt("G").insert_n_curves(8).scale(0.2), Text("表头", color = BLUE).scale(0.8)).arrange(DOWN, buff = SMALL_BUFF), 
            Tex("\\rightarrow").scale(0.8),
            VGroup(PhyEquipTxt("A").scale(0.2), Text("电流表", color = BLUE).scale(0.8)).arrange(DOWN, buff = SMALL_BUFF)
            ).arrange().to_corner(UL)
        lineLeft = PhyElecLine(LEFT * 2, RIGHT * 2).scale(0.5).next_to(phyG, LEFT, buff = -0.04).shift(RIGHT * 2)
        lineRight = PhyElecLine(LEFT * 2, RIGHT * 2).scale(0.5).next_to(phyG, RIGHT, buff = -0.04).shift(RIGHT * 2)
        self.play(Write(txtG2A), phyG.animate.shift(RIGHT * 2), FadeIn(lineLeft), FadeIn(lineRight))

        txt4 = VGroup(
            Text("假设我们要改装的电流表的量程为", t2c = { "量程": BLUE }),
            Tex("0 \\sim I", color = RED_B), Tex("(I>I_{g})")
            ).arrange().scale(0.8).to_edge(DOWN)
        txt4[2][0][1].set_color(RED_B)
        txt4[2][0][3:5].set_color(RED)
        self.play(Write(txt4))
        
        texIg.next_to(phyG, UR, 0)
        texI: Tex = txt4[1][0][2].copy()
        texI.generate_target()
        texI.target.scale(1.5).next_to(lineLeft, UP, aligned_edge = LEFT).shift(RIGHT * 0.2)
        tipI = ArrowTip(width = 0.2, length = 0.2).set_color(RED_B).next_to(texI.target, DOWN).set_y(lineLeft.get_y())
        self.play(FadeIn(texIg, UR * 0.3), MoveToTarget(texI), DrawBorderThenFill(tipI))
        self.wait()

        carrow = CurvedDoubleArrow(texI.get_edge_center(UR), texIg.get_edge_center(UL), angle = -PI * 0.4, color = BLUE)
        ctxt = Text("怎么做到?", color = BLUE).scale(0.8).next_to(carrow, UP)
        self.play(ShowCreation(carrow), Write(ctxt, run_time = 1.6))
        self.wait(1.5)

        txt5 = VGroup(
            Text("由于"), Tex("I>I_{g}"), Text("，因此要将"), 
            Tex("I", color = RED_B), Text("“缩小”为", t2c = { "“缩小”": GOLD }), Tex("I_{g}", color = RED)
            ).arrange().scale(0.8)
        txt5[1][0][0].set_color(RED_B)
        txt5[1][0][2:4].set_color(RED)
        txt6 = Text("同时我们又知道，并联分流", t2c = { "并联": BLUE, "分流": GOLD }).scale(0.8)
        txt7 = Text("因此我们可以将一个较小的电阻并联以分流", t2c = { "较小的电阻": BLUE, "分流": GOLD }).scale(0.8)
        vgTxt5_7 = VGroup(txt5, txt6, txt7).arrange(DOWN).to_edge(DOWN)
        me = VGroup(
            *[PhyElecLine(width = 0.06) for i in range(0, 4)], 
            PhyElecLine(ORIGIN, UP, 0.06), PhyElecLine(ORIGIN, DOWN, 0.06),
            PhyElecLine(ORIGIN, DOWN, 0.06), PhyElecLine(ORIGIN, UP, 0.06)
            ).set_fill(GREY_A)
        me[-2].next_to(me[-1], DOWN, buff = 0)
        Group(me[-1], me[-2]).next_to(me[0], buff = 0)
        me[1].next_to(me[-1], buff = 0, aligned_edge = UP)
        me[2].next_to(me[-2], buff = 0, aligned_edge = DOWN)
        me[-3].next_to(me[1], buff = 0, aligned_edge = UP)
        me[-4].next_to(me[2], buff = 0, aligned_edge = DOWN)
        me[3].next_to(Group(me[-3], me[-4]), buff = 0)
        me.scale(0.7).move_to(ORIGIN).shift(DOWN)
        me2 = me.copy().set_fill(YELLOW)
        for m in me2[0:4]:
            m.stretch(1.4, 1)
        for m in me2[-1:-5:-1]:
            m.stretch(1.4, 0)
        def play_me(me, run_time = 0.2):
            self.play(GrowArrow(me[0]), run_time = run_time)
            self.play(*[GrowArrow(m) for m in me[-1:-3:-1]], run_time = run_time)
            self.play(*[GrowArrow(m) for m in me[1:3]], run_time = run_time)
            self.play(*[GrowArrow(m) for m in me[-3:-5:-1]], run_time = run_time)
            self.play(GrowArrow(me[3]), run_time = run_time)
        gPhyG = Group(phyG, lineLeft, lineRight, texI, tipI, texIg)
        darkrect = Rectangle().set_fill(BLACK, 0.8).set_stroke(width = 0).surround(gPhyG)
        self.play(
            FadeOut(carrow, run_time = 0.3), FadeOut(ctxt, run_time = 0.3), FadeOut(txt4, run_time = 0.3), 
            Write(txt5[:len(txt5) - 1])
            )
        self.play(ReplacementTransform(txt5[-3].copy(), txt5[-1], path_arc = -PI / 2))
        self.wait(0.8)
        self.play(Write(txt6))
        self.play(FadeIn(darkrect))
        play_me(me)
        play_me(me2, 0.4)
        self.remove(me)
        self.play(FadeOut(darkrect), FadeOut(me2))
        self.play(Write(txt7))

        phyR = VGroup(
            PhyEquipR(), PhyElecLine(ORIGIN, LEFT), PhyElecLine(ORIGIN, RIGHT), 
            PhyElecLine(UP, DOWN), PhyElecLine(UP, DOWN)
            )
        phyR[1].next_to(phyR[0], LEFT, 0)
        phyR[2].next_to(phyR[0], buff = 0)
        phyR[3].next_to(phyR[1], LEFT, 0, DOWN)
        phyR[4].next_to(phyR[2], RIGHT, 0, DOWN)
        phyR.scale(0.5).next_to(Group(lineLeft, lineRight), DOWN, 0).shift(UP * 2)
        texIb = Tex("I", font = "宋体", color = RED).scale(0.8).next_to(phyR[0], UR, SMALL_BUFF)
        texIb = VGroup(texIb, Text("并", slant = ITALIC, color = RED).scale(0.5).next_to(texIb, DR, 0).shift(UP * 0.1))
        self.play(FadeIn(phyR, UP * 2), gPhyG.animate.shift(UP * 2))
        self.play(ShowCreationThenFadeAround(phyR[0]), FadeIn(texIb, UR / 2))
        self.wait(0.8)
        self.play(FadeOut(vgTxt5_7))
        
        txt8 = Text("为什么是“较小的电阻”?", t2c = { "“较小的电阻”": BLUE }).scale(0.8)
        txt9 = Text("因为改装的电流表量程通常远大于表头量程", t2c = { "电流表量程": BLUE, "远大于": GOLD, "表头量程": BLUE }).scale(0.8)
        txt10 = VGroup(Text("根据"), Tex("R\\empty=\\frac{U}{I}"), Text("可知")).arrange().scale(0.8)
        txt10[1][0][0].set_color(GREEN)
        txt10[1][0][2].set_color(YELLOW)
        txt10[1][0][4].set_color(RED)
        txt11 = VGroup(Text("当电压一定时，", t2c = { "电压一定": YELLOW }), Tex("I", color = RED), Text("越大，"), Tex("R", color = GREEN), Text("越小")).arrange().scale(0.8)
        vgTxt8_9 = VGroup(txt8, txt9).arrange(DOWN).to_edge(DOWN)
        Group(txt10, txt11).arrange(DOWN).to_edge(DOWN)
        texIL = Tex("I", color = RED_B).scale(0.8).next_to(txt10, UP, MED_LARGE_BUFF)
        texIgL = Tex("I_{g}", color = RED).scale(0.8)
        texIbL = texIb.copy()
        texRgL = Tex("R_{g}", color = GREEN)
        texRbL = Tex("R", color = GREEN)
        texRbL = VGroup(texRbL, Text("并", slant = ITALIC, color = GREEN).scale(0.5).next_to(texRbL, DR, 0).shift(UP * 0.1))
        texLower, texUpper = Tex("<").scale(0.8), Tex(">").scale(0.8)
        lineI = Line().scale(3).set_color(RED_B).next_to(texIL, UP)
        lineIg = Line().scale(3).set_color(RED).next_to(lineI, UP, SMALL_BUFF)
        lineIb = Line().scale(3).set_color(RED_A).scale(0.8).next_to(lineI, UP, SMALL_BUFF, LEFT)
        self.play(FadeIn(txt8, UP))
        self.wait(0.6)
        self.play(Write(txt9))
        self.wait(0.6)
        self.play(vgTxt8_9.animate.scale(0.8).next_to(txtG2A, DOWN, LARGE_BUFF * 2, LEFT), run_time = 0.8)
        self.play(FadeIn(lineI, UP), FadeIn(lineIg, DOWN), FadeIn(texIL, UP))
        self.play(Write(txt10))
        self.play(Write(txt11[:3]), lineIg.animate.scale(0.185, about_point = lineIg.get_right()), GrowArrow(lineIb))
        texIgL.next_to(lineIg, UP)
        texIbL.next_to(lineIb, UP)
        texUpper.move_to((texIgL.get_center() + texIbL.get_center()) / 2)
        self.play(FadeIn(texIgL, DOWN), FadeIn(texIbL, DOWN), FadeIn(texUpper))
        self.wait(0.5)
        self.play(Write(txt11[3:]))
        texRgL.next_to(texIgL, UP)
        texRbL.next_to(texIbL, UP)
        texLower.move_to((texRgL.get_center() + texRbL.get_center()) / 2)
        self.play(FadeIn(texRgL, DOWN), FadeIn(texRbL, DOWN), FadeIn(texLower))
        self.play(ShowCreationThenFadeAround(txt11[-1:-3:-1]), ShowCreationThenFadeAround(txt8[-2:-9:-1]))
        self.wait()
        self.play(*[FadeOut(m) for m in [txt8, txt9, txt10, txt11, lineIg, lineIb, lineI, texIgL, texIbL, texIL, texRgL, texRbL, texUpper, texLower]])
        
        txt12 = VGroup(Text("那么"), texRbL.copy().scale(1 / 0.8), Text("具体如何计算?", t2c = { "计算": GOLD })).arrange().scale(0.8)
        txt13 = VGroup(Text("已知"), Tex("U_{g}=I_{g}\\cdot R_{g}")).arrange().scale(0.8)
        txt13[1][0][0:2].set_color(YELLOW)
        txt13[1][0][3:5].set_color(RED)
        txt13[1][0][6:8].set_color(GREEN)
        txt14 = VGroup(Text("根据并联可知"), texIb.copy().scale(1 / 0.8), Tex("=I-I_{g}")).arrange().scale(0.8)
        txt14[2][0][1].set_color(RED_B)
        txt14[2][0][3:5].set_color(RED)
        txt15 = VGroup(Text("则"), texRbL.copy().scale(1 / 0.8), Tex("="), Tex("\\frac{U_{g}}{A}")).arrange().scale(0.8)
        txt15[3][0][0:2].set_color(YELLOW)
        txt15[3][0][3].set_opacity(0)
        txt15[-1].add(texIbL.copy().next_to(txt15[3][0][2], DOWN, SMALL_BUFF))
        txt15_2 = Tex("\\frac{I_g\\cdot R_g}{I-I_g}").scale(0.8)
        txt15_2[0][0:2].set_color(RED)
        txt15_2[0][3:5].set_color(GREEN)
        txt15_2[0][6].set_color(RED_B)
        txt15_2[0][8:10].set_color(RED)
        txt15_3 = Tex("\\frac{I_g}{I-I_g}R_g").scale(0.8)
        txt15_3[0][0:2].set_color(RED)
        txt15_3[0][3].set_color(RED_B)
        txt15_3[0][5:7].set_color(RED)
        txt15_3[0][7:9].set_color(GREEN)
        txt15_4 = Tex("\\frac{1}{\\frac{I}{I_g}-1}R_g").scale(0.8)
        txt15_4[0][2].set_color(RED_B)
        txt15_4[0][4:6].set_color(RED)
        txt15_4[0][8:10].set_color(GREEN)
        vgTxt13_15 = VGroup(txt13, txt14, txt15).arrange(DOWN, aligned_edge = LEFT)
        vgTxt15_subs = VGroup(txt15_2, txt15_3, txt15_4)
        for m in vgTxt15_subs:
            m.next_to(txt15[3].get_left(), buff = 0)
        txt12UndLine = Underline(txt12)
        txt12UndLine.add_updater(lambda m: m.next_to(txt12, DOWN, SMALL_BUFF))
        self.play(DrawBorderThenFill(txt12))
        self.wait(0.7)
        self.play(txt12.animate.next_to(txtG2A, DOWN, LARGE_BUFF * 1.5, LEFT), GrowArrow(txt12UndLine))
        Group(vgTxt13_15, vgTxt15_subs).next_to(txt12, DOWN, MED_LARGE_BUFF, LEFT)
        self.play(Write(txt13))
        self.wait(0.8)
        self.play(Write(txt14))
        self.wait(0.8)
        self.play(DrawBorderThenFill(txt15))
        for m in vgTxt15_subs:
            self.wait(0.5)
            self.play(Transform(txt15[-1], m))
        self.wait(0.8)

        txt16 = txt15[1:].copy()
        self.play(txt16.animate.move_to(LEFT * 0.5))

        txt17 = VGroup(Text("设缩放倍数", t2c = { "缩放倍数": GOLD }), Tex("n=\\frac{I}{I_g}"))\
            .arrange().scale(0.8).next_to(txt16, DOWN).shift(RIGHT)
        txt17[1][0][0].set_color(GOLD)
        txt17[1][0][2].set_color(RED_B)
        txt17[1][0][4:6].set_color(RED)
        txt18 = Tex("=").scale(0.8).next_to(txt16, buff = SMALL_BUFF)
        txt19 = Tex("\\frac{1}{n-1}R_g").scale(0.8).next_to(txt18, buff = SMALL_BUFF)
        txt19[0][2].set_color(GOLD)
        txt19[0][5:7].set_color(GREEN)
        self.wait(0.5)
        self.play(DrawBorderThenFill(txt17))
        self.wait(0.8)
        self.play(FadeIn(txt18), ReplacementTransform(txt16[-1].copy(), txt19, path_arc = -PI / 2))
        self.play(ShowCreationThenFadeAround(txt19))
        self.wait()

        txt20 = VGroup(texRbL.copy(), txt18.copy(), txt19.copy())
        txt20[1:3].next_to(txt20[0])
        txt20.next_to(txtG2A, DOWN, LARGE_BUFF * 1.5, LEFT)
        self.play(*[FadeOut(m) for m in [txt12, txt12UndLine, vgTxt13_15, txt16, txt17, txt18, txt19]], FadeIn(txt20))
        self.wait(0.5)

        txt21 = VGroup(
            Text("例如，要将一个内阻", t2c = { "内阻": GREEN }), Tex("R_g=6\\Omega", color = GREEN),
            Text("，最大量程", t2c = { "[1:]": RED }), Tex("I_g=3mA", color = RED), Text("的表头")
            ).arrange(buff = 0.2).scale(0.8).next_to(txt20, DOWN, MED_LARGE_BUFF, LEFT).shift(RIGHT)
        txt22 = VGroup(Text("改装为最大量程", t2c = { "最大量程": RED_B }), Tex("I=0.3A", color = RED_B), Text("的电流表"))\
            .arrange(buff = 0.2).scale(0.8).next_to(txt21, DOWN, aligned_edge = LEFT)
        self.play(Write(txt21))
        self.wait(0.5)
        self.play(Write(txt22))

        txt23 = Tex("n=\\frac{I}{I_g}").scale(0.8).next_to(txt22, DOWN, MED_LARGE_BUFF, LEFT)
        txt23[0][0].set_color(GOLD)
        txt23[0][2].set_color(RED_B)
        txt23[0][4:6].set_color(RED)
        txt23_1 = Tex("=").scale(0.8).next_to(txt23, buff = 0.1)
        txt23_2 = Tex("\\frac{0.3A}{3mA}").scale(0.8).next_to(txt23_1, buff = 0.1)
        txt23_2[0][0:4].set_color(RED_B)
        txt23_2[0][5:8].set_color(RED)
        txt23_3 = Tex("\\frac{300mA}{3mA}").scale(0.8).next_to(txt23_1, buff = 0.1)
        txt23_3[0][0:5].set_color(RED_B)
        txt23_3[0][6:9].set_color(RED)
        txt23_4 = Tex("=100").scale(0.8).next_to(txt23_3, buff = 0.1)
        txt23_4[0][1:].set_color(GOLD)
        self.play(Write(txt23))
        self.play(Write(txt23_1), Write(txt23_2))
        self.play(Transform(txt23_2, txt23_3))
        self.play(DrawBorderThenFill(txt23_4))
        self.wait(0.8)

        txt24 = texRbL.copy().next_to(txt23_4, buff = MED_LARGE_BUFF)
        txt24_1 = Tex("=").scale(0.8).next_to(txt24, buff = 0.1)
        txt24_2 = txt19.copy().next_to(txt24_1, buff = 0.1)
        txt24_3 = txt24_1.copy().next_to(txt24_2, buff = 0.1)
        txt24_4 = Tex("\\frac{1}{100-1}R_g").scale(0.8).next_to(txt24_3, buff = 0.1)
        txt24_4[0][2:5].set_color(GOLD)
        txt24_4[0][7:9].set_color(GREEN)
        txt24_5 = Tex("\\frac{6}{99}\\Omega", color = GREEN).scale(0.8).next_to(txt24_3, buff = 0.1)
        self.play(Write(txt24))
        self.play(Write(txt24_1), Write(txt24_2))
        self.play(Write(txt24_3), Write(txt24_4))
        self.wait(0.5)
        self.play(Transform(txt24_4, txt24_5))
        self.play(
            ShowCreationThenFadeAround(Group(txt24, txt24_1, txt24_2, txt24_3, txt24_4)),
            ShowCreationThenFadeAround(phyR[0])
            )
        self.wait()

        self.play(
            *[FadeOut(m) for m in [
                txt20, txt21, txt22, txt23, txt23_1, txt23_2, txt23_4, 
                txt24, txt24_1, txt24_2, txt24_3, txt24_4]
                ]
            )
        
        pme = PhyMaterialEquip("G", grad_up_step = 1, grad_cnt = 3).scale(2).move_to(ORIGIN)
        pme.drtxt = Text("mA", color = RED, font = "Noto Sans Thin").scale(0.8).next_to(pme.surrounding_rect.get_edge_center(DR), UL, SMALL_BUFF)
        pme.add(pme.drtxt)
        self.play(*[FadeOut(m) for m in [gPhyG, phyR, texIb]], FadeIn(pme, UP))

        txt25 = Text("完事后，偷偷将表盘文字改掉").scale(0.8).to_edge(DOWN)
        txt26 = Text("也就是替换为相应的数值和文字即可", color = GREY_A).scale(0.6).to_edge(DOWN)
        self.play(Write(txt25))
        self.play(FadeIn(txt26, UP), txt25.animate.next_to(txt26, UP))
        self.wait(0.5)
        
        vgPmeTransTxt = VGroup()
        pme.generate_nums((0, 3), 0.1, -1, vgPmeTransTxt)
        circle = Circle(color = YELLOW).scale(0.3).move_to(pme.txt).set_stroke(width = 0).set_fill(YELLOW, opacity = 0.3)
        pmeTransDrtxt = Text("A", color = RED, font = "Noto Sans Thin").scale(0.8).next_to(pme.surrounding_rect.get_edge_center(DR), UL, SMALL_BUFF)
        self.play(FadeIn(circle, scale = 0.5))
        self.play(Transform(pme.txt, pme.Txt("A").scale(2).move_to(pme.txt)), run_time = 0.5)
        for i in range(1, len(vgPmeTransTxt)):
            mobj_from = pme.up_nums[i]
            mobj_to = vgPmeTransTxt[i].scale(2).move_to(mobj_from)
            self.play(circle.animate.move_to(mobj_from), run_time = 0.5)
            self.play(Transform(mobj_from, mobj_to), run_time = 0.5)
        self.play(circle.animate.move_to(pme.drtxt))
        self.play(Transform(pme.drtxt, pmeTransDrtxt))
        self.play(FadeOut(circle, scale = 2))
        self.wait()
        self.play(*[FadeOut(m) for m in [txt25, txt26, pme, txtG2A]])

class PhyRefitG2VScene(Scene):
    def construct(self):
        self.add(txtwatermark())

        txtG2V = VGroup(
            VGroup(PhyEquipTxt("G").insert_n_curves(8).scale(0.2), Text("表头", color = BLUE).scale(0.8)).arrange(DOWN, buff = SMALL_BUFF), 
            Tex("\\rightarrow").scale(0.8),
            VGroup(PhyEquipTxt("V").scale(0.2), Text("电压表", color = BLUE).scale(0.8)).arrange(DOWN, buff = SMALL_BUFF)
            ).arrange().to_corner(UL)
        self.play(FadeIn(txtG2V, UP))

        txt1_1 = VGroup(Text("表头", color = BLUE), Tex("\\rightarrow"), Text("电流表", color = BLUE))\
            .arrange(buff = SMALL_BUFF).scale(0.8)
        txt1_2 = VGroup(Text("表头", color = BLUE), Tex("\\rightarrow"), Text("电压表", color = BLUE))\
            .arrange(buff = SMALL_BUFF).scale(0.8)
        txt1_3 = VGroup(Tex("I_g", "\\rightarrow ", "I")).arrange(buff = SMALL_BUFF).scale(0.8)
        txt1_3[0][0].set_color(RED)
        txt1_3[0][2].set_color(RED_B)
        txt1_4 = VGroup(Tex("U_g", "\\rightarrow ", "U")).arrange(buff = SMALL_BUFF).scale(0.8)
        txt1_4[0][0].set_color(YELLOW)
        txt1_4[0][2].set_color(YELLOW_B)
        txt1_5 = Text("并联分流", t2c = { "分流": RED }).scale(0.8)
        txt1_6 = Text("串联分压", t2c = { "分压": YELLOW }).scale(0.8)
        vgTxtGrid = VGroup(txt1_1, txt1_2, txt1_3, txt1_4, txt1_5, txt1_6)\
            .arrange_in_grid(3, 2, v_buff = 0.4, h_buff = 0.6)
        txt2 = Text("对于改装成电流表，我们使用了并联分流的方式", t2c = { "电流表": BLUE, "并联分流": GOLD })\
            .scale(0.8).to_edge(DOWN)
        txt3 = Text("那么改装成电压表要怎么做?", t2c = { "电压表": BLUE }).scale(0.8).to_edge(DOWN)
        txtHow = Text("?").scale(0.8).move_to(txt1_6)
        def SuccessionUseableFadeIn(mobj):
            mobj.generate_target()
            mobj.target.set_opacity(1)
            mobj.set_opacity(0)
            return MoveToTarget(mobj)
        self.play(
            Succession(SuccessionUseableFadeIn(txt1_1), SuccessionUseableFadeIn(txt1_3), SuccessionUseableFadeIn(txt1_5)),
            Write(txt2), run_time = 2
            )
        self.wait()
        self.play(
            Succession(SuccessionUseableFadeIn(txt1_2), SuccessionUseableFadeIn(txt1_4), SuccessionUseableFadeIn(txtHow), run_time = 1.4),
            FadeOut(txt2, run_time = 0.3), Write(txt3, run_time = 1.4)
            )
        self.wait(1.5)
        self.play(ReplacementTransform(txtHow, txt1_6), run_time = 1.2)
        self.play(Indicate(txt1_6))
        self.wait()
        self.play(FadeOut(vgTxtGrid), FadeOut(txt3))

        phyG = PhyEquipTxt("G").scale(0.5)
        phyG.txt.insert_n_curves(8)
        lineLeft = PhyElecLine(LEFT * 2, RIGHT * 2).scale(0.5).next_to(phyG, LEFT, buff = -0.04)
        lineRight = PhyElecLine(LEFT * 2, RIGHT * 2).scale(0.5).next_to(phyG, RIGHT, buff = -0.04)
        gPhyG = VGroup(phyG, lineLeft, lineRight)    # 与PhyRefitG2AScene中的gPhyG结构不同
        self.play(FadeIn(gPhyG, UP))

        txt4 = VGroup(
            Text("假设我们要改装的电压表的量程为", t2c = { "量程": BLUE }),
            Tex("0 \\sim U", "(U>U_g)")
            ).arrange().scale(0.8).to_edge(DOWN)
        txt4[1][0].set_color(YELLOW_B)
        txt4[1][1][1].set_color(YELLOW_B)
        txt4[1][1][3:5].set_color(YELLOW)
        texUg = Tex("U_g", color = YELLOW).scale(0.8).next_to(phyG, UR, -0.1)
        rgU = RangeArrowTex(
            Group(lineLeft, lineRight), "U", 
            lineRight.get_right()[0] - lineLeft.get_left()[0] - 0.2, UP * 2
            )
        rgU.set_color(YELLOW)
        self.play(Write(txt4))
        self.play(FadeIn(texUg, UR * 0.5), FadeIn(rgU, DOWN))