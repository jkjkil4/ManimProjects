import sys
sys.path.append(".")
from manimlib import *
import header


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
        text = "012345678 "
        text2 = ""
        for i in range(10):
            text2 += text
        self.add(Text(text2).scale(0.5))
        self.wait()