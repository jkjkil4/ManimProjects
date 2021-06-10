from manimlib import *

class Elec(Scene):
    def construct(self):
        # Q1的描述文字
        explain1 = VGroup(
            Text("假设有一 点电荷", font_size = 26), 
            TexText("$Q_1$", color = ORANGE, font_size = 26)
            )
        explain1.arrange(RIGHT) # 排列
        explain1.to_corner(UL)  # 移至左上角
        explain1.set_stroke(BLACK, 3, background = True)    # 设置描边
        self.play(Write(explain1))

        # Q1
        elec1 = Circle(radius = 0.1, color = ORANGE)    # 圆
        elec1.set_fill(ORANGE, opacity = 0.5)   # 设置填充颜色
        elec1Label = TexText("$Q_1$", color = ORANGE, font_size = 26)   # 文字
        elec1Label.set_stroke(BLACK, 3, background = True)  # 文字描边
        elec1Label.next_to(elec1, UR, 0)    # 移动文字至elec1右上角
        groupElec1 = VGroup(elec1, elec1Label)
        self.play(Write(groupElec1))
        self.play(groupElec1.animate.shift(LEFT_SIDE / 3), run_time = 1)

        # Q2的描述文字
        explain2 = VGroup(
            Text("和另一 点电荷", font_size = 26),
            TexText("$Q_2$", color = YELLOW, font_size = 26)
            )
        explain2.arrange(RIGHT) # 排列
        # 移至explain1下方
        explain2.next_to(explain1, DOWN)
        explain2.to_edge(LEFT)
        explain2.set_stroke(BLACK, 3, background = True)    # 设置描边
        self.play(Write(explain2))

        # Q2
        elec2 = Circle(radius = 0.1, color = YELLOW)    # 圆
        elec2.set_fill(YELLOW, opacity = 0.5)   # 设置填充颜色
        elec2Label = TexText("$Q_2$", color = YELLOW, font_size = 26)   # 文字
        elec2Label.set_stroke(BLACK, 3, background = True)  # 文字描边
        elec2Label.next_to(elec2, UR, 0)    # 移动文字至elec2右上角
        groupElec2 = VGroup(elec2, elec2Label)
        self.play(Write(groupElec2))
        self.play(groupElec2.animate.shift(RIGHT_SIDE / 3), run_time = 1)

        # 虚线
        dashedLine = DashedLine(LEFT_SIDE, RIGHT_SIDE, color = BLUE)
        dashedLine.set_opacity(0.4) # 设置透明度
        self.play(
            VGroup(explain1, explain2).animate.scale(0.8, about_edge = UL).set_opacity(0.6),
            Write(dashedLine),
            run_time = 1.5
            )

        self.wait()