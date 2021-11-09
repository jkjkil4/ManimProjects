import sys
sys.path.append(".")
from manimlib import *
import header

class Test(Scene):
    def construct(self):
        txt = TexText("This is a text with $\\LaTeXe$ part.")
        self.play(Write(txt))

class ThreeDTest(Scene):
    def construct(self):
        # 设置视角
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )
        # frame.focal_distance = 100

        def updater1(m):
            m.rotate(DEGREES / 4)
        frame.add_updater(updater1)

        val = ValueTracker(2)
        def updater2(m):
            m.focal_distance = val.get_value()
        frame.add_updater(updater2)

        num = DecimalNumber(2)
        num.add_updater(lambda m: num.set_value(float(frame.focal_distance)))

        m1 = Cube(color = RED, gloss = 0.4, shadow = 0.2).stretch(0.5, 2, about_edge = OUT)
        # #         0    1     2      3       4       5
        # colors = (RED, BLUE, GREEN, ORANGE, PURPLE, GOLD)
        # for mobj, color in zip(m1, colors):
        #     mobj.set_color(color)
        # m1[-1].set_color([RED, GREEN, BLUE, WHITE])
        m2 = Cube(color = BLUE, gloss = 0.4, shadow = 0.2).stretch(0.5, 2, about_edge = IN)
        m3 = Square()
        txt = VGroup(Text("frame.focal_distance:"), num).arrange().to_corner(UL).fix_in_frame()
        self.add(txt)
        self.play(FadeIn(m1, IN), FadeIn(m2, OUT))
        self.play(m1.animate.shift(OUT), m2.animate.shift(IN), FadeIn(m3, scale = 0.5))
        self.play(val.animate.set_value(30), rate_func = rush_into, run_time = 2)
        self.wait()
        self.play(val.animate.set_value(0.4), rate_func = rush_from, run_time = 2)
        self.wait()
        


# class NumberPlaneScene(Scene):
#     def construct(self):
#         nump = NumberPlane((-12, 12), (-12, 12))
#         sqrGraph = nump.get_graph(lambda x: x ** 2, color = GREEN)
#         derGraph = nump.get_graph(lambda x: 2 * x - 1, color = ORANGE)
#         dot = Dot([1, 1, 0], color = ORANGE)
#         matrix = [[1, 0.5], [0, 1]]
#         group = Group(nump, sqrGraph, derGraph, dot)
#         self.play(ShowCreation(nump, lag_ratio = 0.01), run_time = 1.5)
#         self.play(ShowCreation(sqrGraph))
#         self.wait(0.5)
#         self.play(Write(dot), FocusOn(dot.get_center()))
#         self.play(ShowCreation(derGraph))
#         self.wait()
#         self.play(group.animate.apply_matrix(matrix), run_time = 2)
#         self.play(Flash(dot, line_length = 0.15))
#         self.wait()

'''
class Test(Scene):
    def construct(self):
        xRad = int(FRAME_X_RADIUS)
        yRad = int(FRAME_Y_RADIUS)
        circles = []
        for j in eqRange(-yRad, yRad, 2):
            for i in eqRange(-xRad, xRad, 2):
                circle = Circle(radius = 1, color = GREEN)
                circle.shift([i, j, 0])
                circles.append(circle)
        for circle in circles:
            self.play(Write(circle), run_time = 0.05)
        for circle in circles:
            self.play(circle.animate.set_opacity(1), run_time = 0.05)
            self.play(circle.animate.set_opacity(0.5), run_time = 0.05)
            circle.set_color(RED)

class Vec(Scene):
    def construct(self):
        plane = NumberPlane((-12, 12), (-12, 12), color = BLUE)
        plane.add_coordinate_labels(eqRange(-11, 11, 2), eqRange(-11, 11, 2), color = BLUE_C)
        tanGraph = plane.get_graph(lambda x: np.tan(x), color = GREEN)
        group = Group(plane, tanGraph)
        matrix = [[1, -1], [0, 1]]
        self.play(ShowCreation(plane, lag_ratio = 0.01), run_time = 1.5)
        self.play(ShowCreation(tanGraph))
        self.play(group.animate.apply_matrix(matrix), run_time = 2)

class Test2(Scene):
    def construct(self):
        circle = Circle()
        circle.shift(UL)
        self.add(circle)
        self.play(ShowCreationThenFadeAround(circle), run_time = 3)
        self.wait()

class Test3(Scene):
    def construct(self):
        str1 = "abcbdadcbddcabcba中文"
        group = VGroup(Text(str1).set_color(BLUE), Text(str1).set_color(BLUE))
        group.arrange(buff = SMALL_BUFF, aligned_edge = DOWN)
        self.play(Write(group), run_time = 10)
'''
