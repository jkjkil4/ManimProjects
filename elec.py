import sys
sys.path.append(".")
import header as h
from manimlib import *

def createLabel(tex, col):
    label = Tex(tex, color = col) # 文字
    label.set_stroke(BLACK, 3, background = True)   # 文字描边
    return label
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
            )
        explainQ1.arrange(RIGHT) # 排列
        explainQ1.to_corner(UL)  # 移至左上角
        explainQ1.set_stroke(BLACK, 3, background = True)    # 设置描边
        self.play(Write(explainQ1))

        # Q1
        elec1, elec1Label = createElecWithLabel("Q_1", ORANGE)
        groupElec1 = VGroup(elec1, elec1Label)
        self.play(Write(groupElec1))
        self.play(groupElec1.animate.shift(LEFT_SIDE / 4), run_time = 1)

        # Q2的描述文字
        explainQ2 = VGroup(
            Text("和另一 点电荷"),
            Tex("Q_2", color = YELLOW)
            )
        explainQ2.arrange(RIGHT) # 排列
        explainQ2.next_to(explainQ1, DOWN, aligned_edge = LEFT) # 移至explain1下方
        explainQ2.set_stroke(BLACK, 3, background = True)    # 设置描边
        self.play(Write(explainQ2))

        # Q2
        elec2, elec2Label = createElecWithLabel("Q_2", YELLOW)
        groupElec2 = VGroup(elec2, elec2Label)  # 描述
        self.play(Write(groupElec2))
        self.play(groupElec2.animate.shift(RIGHT_SIDE / 4), run_time = 1)
        self.wait(0.5)

        # 关于两个点电荷正负性与受力方向的描述
        explainF1 = Text("我们知道 \"同号电荷相斥、异号电荷相吸\"")
        explainF1.shift(UP)
        self.play(
            FadeIn(explainF1, shift = UP), 
            VGroup(explainQ1, explainQ2).animate.scale(0.7, about_edge = UL).set_opacity(0.6), 
            run_time = 1)
        self.wait(2)
        explainF2 = Text("也就是说 同号电荷之间受力指向外部、异号电荷受力指向内部").move_to(explainF1)
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
        self.bring_to_back(elec1Arrow, elec2Arrow)  # 置于底层
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
            run_time = 1.5
            )
        
        # 再次演示
        elecChanges(0.6, 0.1)
        self.wait(0.5)

        # 隐藏部分内容
        self.play(FadeOut(signCircle1), FadeOut(signCircle2), FadeOut(elec1Arrow), FadeOut(elec2Arrow), run_time = 0.7)

        self.wait()