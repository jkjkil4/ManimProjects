from header import *

class Elec(Scene):
    def construct(self):
        explain1 = VGroup(
            Text("假设有一 点电荷", font_size = 26), 
            TexText("$Q_1$", color = ORANGE, font_size = 26)
            )
        explain1.arrange(RIGHT)
        explain1.to_corner(UL)
        explain1.set_stroke(BLACK, 3, background = True)
        self.play(Write(explain1))

        elec1 = Circle(radius = 0.12, color = ORANGE)
        elec1.set_fill(ORANGE, opacity = 0.5)
        elec1Label = TexText("$Q_1$", color = ORANGE, font_size = 26)
        elec1Label.set_stroke(BLACK, 3, background = True)
        elec1Label.next_to(elec1, UR, 0)
        groupElec1 = VGroup(elec1, elec1Label)
        self.play(Write(groupElec1))
        self.play(groupElec1.animate.shift(LEFT_SIDE / 3), run_time = 1)

        explain2 = VGroup(
            Text("和另一 点电荷", font_size = 26),
            TexText("$Q_2$", color = YELLOW, font_size = 26)
            )
        explain2.arrange(RIGHT)
        explain2.next_to(explain1, DOWN)
        explain2.to_edge(LEFT)
        explain2.set_stroke(BLACK, 3, background = True)
        self.play(Write(explain2))

        elec2 = Circle(radius = 0.12, color = YELLOW)
        elec2.set_fill(YELLOW, opacity = 0.5)
        elec2Label = TexText("$Q_2$", color = YELLOW, font_size = 26)
        elec2Label.set_stroke(BLACK, 3, background = True)
        elec2Label.next_to(elec2, UR, 0)
        groupElec2 = VGroup(elec2, elec2Label)
        self.play(Write(groupElec2))
        self.play(groupElec2.animate.shift(RIGHT_SIDE / 3), run_time = 1)
        
        self.wait()