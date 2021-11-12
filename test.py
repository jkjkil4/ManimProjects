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
        cube = VCube()
        cylinder = Cylinder().scale(0.5).stretch(4, 2)
        self.add(cube, cylinder)


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
