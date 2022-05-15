import sys
sys.path.append(".")
from manimlib import *
import header

class Test(Scene):
    def construct(self):
        vg1 = VGroup(*[Circle() for _ in range(4)])
        vg2 = VGroup(*[Line() for _ in range(4)])
        for a, b in zip(vg1.submobjects, vg2.submobjects):
            print(type(vg1), type(vg2))
        vg1.become(vg2)
        for a, b in zip(vg1.submobjects, vg2.submobjects):
            print(type(vg1), type(vg2))

class ThreeDTest(Scene):
    def construct(self):
        cube = VCube()
        cylinder = Cylinder().scale(0.5).stretch(4, 2)
        self.add(cube, cylinder)


class A(Scene):
    def construct(self):
        vec1 = np.array([2, 3, 4])
        mat1 = np.array([
            [4, 3, 2],
            [1, 9, 4],
            [4, 8, 2]
        ])
        result = np.matmul(mat1, vec1)
        print(result)

class ParametricSurfaceTest(Scene):
    def construct(self):
        def uv_func(u, v) -> np.array:
            return np.array([u, v, 1 / v])
        surf = ParametricSurface(uv_func, (-3, 3), (-3, 3))

        frame = self.camera.frame
        frame.set_euler_angles(theta = 12 * DEGREES, phi = 70 * DEGREES)

        self.add(surf)

class AnimatedStreamLinesExample(Scene):
    def construct(self):
        coord = Axes(x_range=[-7, 7, 1], width=14,
                     y_range=[-4, 4, 1], height=8)
        s = StreamLines(
            lambda x, y: (x * 0.7 + y * 0.5, y * 0.7 - x * 0.5),
            coord,
            magnitude_range=(0.5, 5)
        )
        asl = AnimatedStreamLines(s)
        self.add(coord, asl)
        self.wait(5)


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
