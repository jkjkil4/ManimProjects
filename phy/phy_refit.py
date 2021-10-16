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
        self.play(*[ReplacementTransform(txt2[3:5].copy(), tex) for tex in [phyGTex, phyATex, phyVTex]])
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

class PhyRefitScene(Scene):
    def construct(self):
        self.add(txtwatermark())

        phyG = PhyEquipTxt("G").scale(0.5)
        phyG.txt.insert_n_curves(8)
        self.play(FadeIn(phyG))

        txt1 = Text("表头的量程相当的小", t2c = { "表头": BLUE }).scale(0.8)
        txt2 = Text("可以通过改装将其变为常用的量程相对较大的电流表和电压表", t2c = { "电流表": BLUE, "电压表": BLUE }).scale(0.8)
        Group(txt1, txt2).arrange(DOWN).to_edge(DOWN)
        self.play(Write(txt1))
        self.play(Write(txt2))
        self.wait()

        txt3 = Text("在这之前，我们要知道表头的几个基本属性", t2c = { "基本属性": BLUE }).scale(0.8).to_corner(DOWN)
        self.play(FadeOut(txt1, run_time = 0.3), FadeOut(txt2, run_time = 0.3), Write(txt3))

        phyArwG = PhyArrowEquip(grad_up_range = (-2, -2), grad_up_num_step = 0, grad_zero_offset = -2)\
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
        self.play(phyArwG.arrow_offset.animate.set_value(40))
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
        lineLeft = PhyElecLine().scale(0.5).next_to(phyG, LEFT, buff = -0.04).shift(RIGHT * 2)
        lineRight = PhyElecLine().scale(0.5).next_to(phyG, RIGHT, buff = -0.04).shift(RIGHT * 2)
        self.play(Write(txtG2A), phyG.animate.shift(RIGHT * 2), FadeIn(lineLeft), FadeIn(lineRight))



        # phyG_M = PhyMaterialEquip("G", grad_up_num_step = 1, bottom_rect_height = 0.3).scale(1.5)
        # phyG_M.nums.set_opacity(0)
        # phyG_Txt = Text("表头", color = BLUE).scale(0.6).next_to(phyG_M.get_edge_center(UR), DL, SMALL_BUFF)
        # phyG = VGroup(phyG_M, phyG_Txt)
        # self.play(FadeIn(phyG, UP))
        

