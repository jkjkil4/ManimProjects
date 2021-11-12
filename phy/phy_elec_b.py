import sys
sys.path.append('.')
from manimlib import *
from header import *

def complex_to_ndarray(num: complex, c1: int, c2: int):
    def getv(ind: int):
        if c1 == ind:
            return num.real
        if c2 == ind:
            return num.imag
        return 0
    return np.array((getv(0), getv(1), getv(2)))

class RCurve(ParametricCurve):
    def __init__(self, r = 1, w = 4.5, height = 1, **kwargs):
        super().__init__(
            lambda t: r * complex_to_R3(np.exp(1j * w * t)) + OUT * t * height / TAU,
            t_min = 0, t_max = TAU, **kwargs
            )
        self.move_to(ORIGIN)

class Battery(VGroup):
    CONFIG = {
        "line_po_len": 1,
        "line_ne_len": 0.6,
        "line_buff": 0.2,
        "line_config": {}
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.linePo = Line(ORIGIN, DOWN * self.line_po_len, **self.line_config)
        self.lineNe = Line(ORIGIN, DOWN * self.line_ne_len, **self.line_config)
        self.add(self.lineNe, self.linePo).arrange(RIGHT, buff = self.line_buff)


class TestScene(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(theta = 10 * DEGREES, phi = 70 * DEGREES)
        def frame_updater(frame):
            frame.increment_theta(DEGREES / 40)
            self.update_sort_by_camera_distance()
        frame.add_updater(frame_updater)
        
        self.add(txtwatermark().fix_in_frame())

        r_curve = RCurve(height = 6, w = 10.5, step_size = DEGREES, color = GOLD)\
            .apply_depth_test().rotate(90 * DEGREES, axis = UP).rotate(-90 * DEGREES, axis = LEFT).shift(OUT)
        battery = Battery().apply_depth_test().shift(IN * 2)
        linePo, lineNe = VMobject().apply_depth_test(), VMobject().apply_depth_test()
        linePo.set_points((r_curve.get_end(), r_curve.get_right() + IN * 3, battery.linePo.get_center()))
        lineNe.set_points((r_curve.get_start(), r_curve.get_left() + IN * 3, battery.lineNe.get_center()))
        linePo.asbcd_fn, lineNe.asbcd_fn = linePo.get_start, lineNe.get_start
        self.play(ShowCreation(r_curve))

        txt1 = Text("这是一个由导线绕成的螺线").scale(0.8).to_edge(DOWN).fix_in_frame()
        self.play(Write(txt1))

        self.play(*map(ShowCreation, (battery, linePo, lineNe)))

