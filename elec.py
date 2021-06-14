import sys
sys.path.append(".")
import header as h
from manimlib import *

defaultFontSize = 24

def createLabel(tex, col):
    return Tex(tex, color = col)
def createElecWithLabel(tex, col):
    elec = Circle(radius = 0.1, color = col)    # 圆
    elec.set_fill(col, opacity = 0.5)   # 设置填充颜色
    label = createLabel(tex, col)
    label.next_to(elec, UR, 0)
    return elec, label

class Elec(Scene):
    def construct(self):
        # Q1的描述文字
        explainQ1 = VGroup(
            Text("假设有一 点电荷"), 
            Tex("Q_1", color = ORANGE)
            ).arrange().to_corner(UL)
        self.play(Write(explainQ1))

        # Q1
        elec1, elec1Label = createElecWithLabel("Q_1", ORANGE)
        groupElec1 = VGroup(elec1, elec1Label)
        self.play(Write(groupElec1))
        self.play(groupElec1.animate.shift(LEFT * 2), run_time = 1)

        # Q2的描述文字
        explainQ2 = VGroup(
            Text("和另一 点电荷"),
            Tex("Q_2", color = YELLOW)
            ).arrange().next_to(explainQ1, DOWN, aligned_edge = LEFT)
        self.play(Write(explainQ2))

        # Q2
        elec2, elec2Label = createElecWithLabel("Q_2", YELLOW)
        groupElec2 = VGroup(elec2, elec2Label)  # 描述
        self.play(Write(groupElec2))
        self.play(groupElec2.animate.shift(RIGHT * 2), run_time = 1)
        self.wait(0.5)

        # 关于两个点电荷正负性与受力方向的描述
        explainF1 = Text("我们知道 \"同号电荷相斥、异号电荷相吸\"")
        explainF1.shift(UP)
        self.play(
            FadeIn(explainF1, shift = UP), 
            VGroup(explainQ1, explainQ2).animate.scale(0.7, about_edge = UL).set_opacity(0.6), 
            run_time = 1)
        self.wait(2)
        explainF2 = Text("也就是说 同号电荷之间静电力指向外部、异号电荷静电力指向内部").move_to(explainF1)
        self.play(ReplacementTransform(explainF1, explainF2))
        self.wait()

        # 用来标识正负的圆
        signCircle1 = Circle(radius = 0.2, color = RED).move_to(elec1)
        signCircle2 = Circle(radius = 0.2, color = RED).move_to(elec2)
        def signCircleAnimate(sc, q):   # 切换颜色的动画
            return sc.animate.set_stroke(color = RED if q > 0 else BLUE)
        self.bring_to_back(signCircle1, signCircle2)    # 置于底层
        self.play(Write(signCircle1), Write(signCircle2), run_time = 0.5)   # 显示

        # 力的方向
        elec1Arrow = Arrow(h.getPos(elec1), h.getPos(elec1), buff = 0, fill_color = GOLD)
        elec2Arrow = Arrow(h.getPos(elec2), h.getPos(elec2), buff = 0, fill_color = GOLD)
        def arrowAnimate(arrow, elec, defOffset, scale = 1):    # 改变力的方向的动画
            return arrow.animate.set_points_by_ends(h.getPos(elec), h.getPos(elec) + defOffset * scale)
        self.play(arrowAnimate(elec1Arrow, elec1, LEFT), arrowAnimate(elec2Arrow, elec2, RIGHT), run_time = 0.8)    # 显示
        self.wait()

        def elecChanges(runTime, waitTime = DEFAULT_WAIT_TIME):  # 切换正负，播放动画
            q1, q2 = -1, 1
            self.play(
                signCircleAnimate(signCircle1, q1), signCircleAnimate(signCircle2, q2),
                arrowAnimate(elec1Arrow, elec1, LEFT, -1), arrowAnimate(elec2Arrow, elec2, RIGHT, -1),
                run_time = runTime)
            self.wait(waitTime)

            q2 = -1
            self.play(
                signCircleAnimate(signCircle2, q2),
                arrowAnimate(elec1Arrow, elec1, LEFT), arrowAnimate(elec2Arrow, elec2, RIGHT),
                run_time = runTime)
            self.wait(waitTime)

            q1 = 1
            self.play(
                signCircleAnimate(signCircle1, q1),
                arrowAnimate(elec1Arrow, elec1, LEFT, -1), arrowAnimate(elec2Arrow, elec2, RIGHT, -1),
                run_time = runTime)
            self.wait(waitTime)

            q2 = 1
            self.play(
                signCircleAnimate(signCircle2, q2),
                arrowAnimate(elec1Arrow, elec1, LEFT), arrowAnimate(elec2Arrow, elec2, RIGHT),
                run_time = runTime)
            self.wait(waitTime)
        elecChanges(0.7)

        # 虚线
        dashedLine = DashedLine(LEFT_SIDE, RIGHT_SIDE, color = GOLD)
        dashedLine.set_opacity(0.5) # 设置透明度
        self.bring_to_back(dashedLine)  # 置于底层
        explainF3 = Text("并且 力位于二者所在的直线上").move_to(explainF2)
        self.play(
            Write(dashedLine),
            FadeTransform(explainF2, explainF3),
            run_time = 1.5)
        
        # 再次演示
        elecChanges(0.7, 0.1)
        self.wait(0.5)

        # 隐藏部分内容
        self.play(
            FadeOut(signCircle1), FadeOut(signCircle2), 
            FadeOut(elec1Arrow), FadeOut(elec2Arrow),
            FadeOut(explainF3),
            run_time = 0.7)
        self.wait(0.5)

        # d
        explainD = VGroup(
            Tex("Q_1", color = ORANGE), Text("与"), Tex("Q_2", color = YELLOW), 
            Text("之间距离为"), Tex("d", color = GREEN)
            ).arrange().next_to(explainQ2, DOWN, aligned_edge = LEFT)
        dLine = Line(h.getPos(elec1), h.getPos(elec2), color = GREEN, buff = 0.05).set_opacity(0.75)
        d = Tex("d", color = GREEN).next_to(dLine, UP)
        self.play(Write(explainD), Write(d), FadeOut(dashedLine), FadeIn(dLine))
        self.play(VGroup(groupElec1, groupElec2, dLine, d).animate.shift(DOWN), run_time = 0.7)
        VGroup(elec1Arrow, elec2Arrow).shift(DOWN)
        self.wait()

        # 公式
        formula = Tex("F=k\\frac{Q_1 Q_2}{d^2}", font_size = defaultFontSize * 2)
        formulaQ1 = VGroup(formula[0][3], formula[0][4])
        formulaQ2 = VGroup(formula[0][5], formula[0][6])
        for single in [formula[0][i] for i in [0, 1, 2, 7, 8, 9]] + [formulaQ1, formulaQ2]:
            single.scale(0.75)
        for change in [[0, GOLD], [2, PURPLE], [3, ORANGE], [4, ORANGE], [5, YELLOW], [6, YELLOW], [8, GREEN]]:
            formula[0][change[0]].set_fill(change[1])
        formula.next_to(d, UP, MED_LARGE_BUFF)
        # 文字
        explainFormula = Text("两电荷之间静电力公式为")
        explainFormula.next_to(formula, UP)
        self.play(explainD.animate.scale(0.7, about_edge = UL).set_opacity(0.6), Write(explainFormula))
        self.play(FadeIn(formula, DOWN))
        self.wait(0.5)

        # F
        explainFormulaF = VGroup(
            Tex("F", color = GOLD).scale(1.5), Text("静电力"),
            VGroup(Text("单位"), Tex("N", color = GOLD).scale(1.5)).arrange()
            ).arrange().to_edge(UP).shift(3.5 * RIGHT)
        explainFormulaF[2].scale(0.8).next_to(explainFormulaF[1], RIGHT, aligned_edge = DOWN)
        symbolF1 = Tex("F", color = GOLD)
        symbolF2 = Tex("F", color = GOLD)
        f_always(symbolF1.next_to, elec1Arrow.get_end, lambda:LEFT, lambda:0)
        f_always(symbolF2.next_to, elec2Arrow.get_end, lambda:RIGHT, lambda:0)
        self.play(FadeOut(explainFormula))
        self.wait(0.5)
        self.play(
            Indicate(formula[0][0]), Write(explainFormulaF),
            FadeIn(elec1Arrow), FadeIn(elec2Arrow), FadeIn(symbolF1), FadeIn(symbolF2), 
            run_time = 1)
        self.wait(1.5)
        # k
        explainFormulaK = VGroup(
            Tex("k", color = PURPLE).scale(1.5), Text("静电力常量"), 
            VGroup(Text("其值约为"), Tex("9\\times 10^9", color = PURPLE).scale(1.5)).arrange()
            ).arrange().next_to(explainFormulaF, DOWN, aligned_edge = LEFT)
        explainFormulaK[2].scale(0.8).next_to(explainFormulaK[1], RIGHT, aligned_edge = DOWN)
        self.play(Indicate(formula[0][2]), Write(explainFormulaK), run_time = 1)
        self.wait(2)
        # Q
        explainFormulaQ = VGroup(
            Tex("Q_1", color = ORANGE).scale(1.5), Tex("Q_2", color = YELLOW).scale(1.5), Text("电荷量大小"),
            VGroup(Text("单位"), Tex("C", color = "#FFC217").scale(1.5)).arrange()
            ).arrange().next_to(explainFormulaK, DOWN, aligned_edge = LEFT)
        explainFormulaQ[3].scale(0.8).next_to(explainFormulaQ[2], RIGHT, aligned_edge = DOWN)
        self.play(Indicate(formulaQ1), Indicate(formulaQ2), Write(explainFormulaQ), run_time = 1)
        self.wait(2)
        # d
        explainFormulaD = VGroup(
            Tex("d", color = GREEN).scale(1.5), Text("二者之间距离"),
            VGroup(Text("单位"), Tex("m", color = GREEN).scale(1.5)).arrange()
            ).arrange().next_to(explainFormulaQ, DOWN, aligned_edge = LEFT)
        explainFormulaD[2].scale(0.8).next_to(explainFormulaD[1], RIGHT, aligned_edge = DOWN)
        self.play(Indicate(formula[0][8]), Write(explainFormulaD), run_time = 1)
        self.wait(2)
        
        # 缩小
        explainFormulaArgs = VGroup(explainFormulaF, explainFormulaK, explainFormulaQ, explainFormulaD)
        self.play(explainFormulaArgs.animate.scale(0.7, about_edge = UR), run_time = 1)

        # 改变 d
        explainChangeD1 = VGroup(
            Text("当"), Tex("d", color = GREEN).scale(1.5), Text("增大", color = RED), Text("时 "),
            Tex("F", color = GOLD).scale(1.5), Text("随之"), Text("减小", color = BLUE)
            ).arrange().next_to(dLine, DOWN, MED_LARGE_BUFF)
        f_always(dLine.set_points_by_ends, lambda: h.getPos(elec1), lambda: h.getPos(elec2))
        self.play(FadeIn(explainChangeD1, UP))
        self.wait(0.7)
        self.play(
            CircleIndicate(formula[0][8]), CircleIndicate(formula[0][0]),
            formula[0][8].animate.scale(4 / 3), formula[0][0].animate.scale(2 / 3),
            groupElec1.animate.shift(LEFT), groupElec2.animate.shift(RIGHT),
            elec1Arrow.animate.set_points_by_ends(h.getPos(elec1) + LEFT, h.getPos(elec1) + LEFT * 1.7),
            elec2Arrow.animate.set_points_by_ends(h.getPos(elec2) + RIGHT, h.getPos(elec2) + RIGHT * 1.7),
            run_time = 3)
        self.wait(0.7)
        explainChangeD2 = VGroup(
            Text("当"), Tex("d", color = GREEN).scale(1.5), Text("减小", color = BLUE), Text("时 "),
            Tex("F", color = GOLD).scale(1.5), Text("随之"), Text("增大", color = RED)
            ).arrange().next_to(dLine, DOWN, MED_LARGE_BUFF)
        self.play(ReplacementTransform(explainChangeD1, explainChangeD2), run_time = 0.5)
        self.play(
            CircleIndicate(formula[0][8]), CircleIndicate(formula[0][0]),
            formula[0][8].animate.scale(0.75), formula[0][0].animate.scale(1.5),
            groupElec1.animate.shift(RIGHT), groupElec2.animate.shift(LEFT),
            elec1Arrow.animate.set_points_by_ends(h.getPos(elec1) + RIGHT, h.getPos(elec1)),
            elec2Arrow.animate.set_points_by_ends(h.getPos(elec2) + LEFT, h.getPos(elec2)),
            run_time = 3)
        self.wait(2)

        # 改变 Q1
        explainChangeQ1 = VGroup(
            Text("当"), Tex("Q_1", color = ORANGE).scale(1.5), Text("增大", color = RED), Text("时 "),
            Tex("F", color = GOLD).scale(1.5), Text("随之"), Text("增大", color = RED)
            ).arrange().next_to(dLine, DOWN, MED_LARGE_BUFF)
        self.play(FadeTransform(explainChangeD2, explainChangeQ1))
        self.wait(0.7)
        self.play(
            CircleIndicate(formula[0][3]), CircleIndicate(formula[0][0]),
            formulaQ1.animate.scale(1.5), formula[0][0].animate.scale(1.5),
            elec1Label.animate.scale(1.5, about_edge = DL),
            arrowAnimate(elec1Arrow, elec1, LEFT, 1.5), arrowAnimate(elec2Arrow, elec2, RIGHT, 1.5),
            run_time = 3)
        self.wait(0.7)
        explainChangeQ2 = VGroup(
            Text("当"), Tex("Q_1", color = ORANGE).scale(1.5), Text("减小", color = BLUE), Text("时 "),
            Tex("F", color = GOLD).scale(1.5), Text("随之"), Text("减小", color = BLUE)
            ).arrange().next_to(dLine, DOWN, MED_LARGE_BUFF)
        self.play(ReplacementTransform(explainChangeQ1, explainChangeQ2), run_time = 0.5)
        self.play(
            CircleIndicate(formula[0][3]), CircleIndicate(formula[0][0]),
            formulaQ1.animate.scale(2 / 3), formula[0][0].animate.scale(2 / 3),
            elec1Label.animate.scale(2 / 3, about_edge = DL),
            arrowAnimate(elec1Arrow, elec1, LEFT, 1), arrowAnimate(elec2Arrow, elec2, RIGHT, 1),
            run_time = 3)
        self.wait(1)

        # 同理
        explainSame = VGroup(Tex("Q_2", color = YELLOW).scale(1.5), Text("同理")).arrange().next_to(dLine, DOWN, MED_LARGE_BUFF)
        self.play(Transform(explainChangeQ2, explainSame))
        self.wait(1)
        self.play(*[FadeOut(mobject) for mobject in self.mobjects])
        self.wait(0.5)