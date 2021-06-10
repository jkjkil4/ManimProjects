from manimlib import *

fontSize = 24

def createLabel(tex, col):
    label = TexText(tex, color = col, font_size = fontSize) # 文字
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
            Text("假设有一 点电荷", font_size = fontSize), 
            TexText("$Q_1$", color = ORANGE, font_size = fontSize)
            )
        explainQ1.arrange(RIGHT) # 排列
        explainQ1.to_corner(UL)  # 移至左上角
        explainQ1.set_stroke(BLACK, 3, background = True)    # 设置描边
        self.play(Write(explainQ1))

        # Q1
        elec1, elec1Label = createElecWithLabel("$Q_1$", ORANGE)
        groupElec1 = VGroup(elec1, elec1Label)
        self.play(Write(groupElec1))
        self.play(groupElec1.animate.shift(LEFT_SIDE / 3), run_time = 1)

        # Q2的描述文字
        explainQ2 = VGroup(
            Text("和另一 点电荷", font_size = fontSize),
            TexText("$Q_2$", color = YELLOW, font_size = fontSize)
            )
        explainQ2.arrange(RIGHT) # 排列
        explainQ2.next_to(explainQ1, DOWN, aligned_edge = LEFT) # 移至explain1下方
        explainQ2.set_stroke(BLACK, 3, background = True)    # 设置描边
        self.play(Write(explainQ2))

        # Q2
        elec2, elec2Label = createElecWithLabel("$Q_2$", YELLOW)
        groupElec2 = VGroup(elec2, elec2Label)  # 描述
        self.play(Write(groupElec2))
        self.play(groupElec2.animate.shift(RIGHT_SIDE / 3), run_time = 1)
        self.wait()

        # # 关于两个点电荷正负性与受力方向的描述
        # explainF1 = Text("我们知道 \"同号电荷相斥、异号电荷相吸\"", font_size = fontSize)
        # explainF1.shift(UP)
        # self.play(FadeIn(explainF1), run_time = 1)
        # self.wait()

        # # 虚线
        # dashedLine = DashedLine(LEFT_SIDE, RIGHT_SIDE, color = BLUE)
        # dashedLine.set_opacity(0.5) # 设置透明度
        # self.bring_to_back(dashedLine)  # 置于底层
        # # 描述
        # explainLine = Text("也就是说 当")
        # self.play(
        #     FadeOut(explainF1), 
        #     VGroup(explainQ1, explainQ2).animate.scale(0.8, about_edge = UL).set_opacity(0.6),
        #     Write(dashedLine),
        #     run_time = 1.5
        #     )

        self.wait()