import sys
sys.path.append('.')
from manimlib import *
from header import *

class TestScene(Scene):

    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(theta = 20 * DEGREES, phi = 70 * DEGREES)

        r = 2
        w = 4
        spiral_line = ParametricCurve(
            lambda t: r * complex_to_R3(np.exp(1j * w * t)) + OUT * t / 3,
            t_min = 0, t_max = TAU * 1.5, color = RED, stroke_width = 8
            ).shift(IN * 2.5)
        self.play(ShowCreation(spiral_line), run_time = 3)
        self.play(spiral_line.animate.stretch(0.5, 2, about_point = spiral_line.get_nadir()), rate_func = rush_from)
        self.play(spiral_line.animate.stretch(2, 2, about_point = spiral_line.get_nadir()))
