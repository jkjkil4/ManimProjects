import sys
sys.path.append('.')
from manimlib import *
from header import *

# def complex_to_ndarray(num: complex, c1: int, c2: int):
#     def getv(ind: int):
#         if c1 == ind:
#             return num.real
#         if c2 == ind:
#             return num.imag
#         return 0
#     return np.array((getv(0), getv(1), getv(2)))

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
        "line_ne_len": 0.5,
        "line_buff": 0.2,
        "line_config": {}
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.linePo = Line(ORIGIN, DOWN * self.line_po_len, **self.line_config)
        self.lineNe = Line(ORIGIN, DOWN * self.line_ne_len, **self.line_config)
        self.add(self.lineNe, self.linePo).arrange(RIGHT, buff = self.line_buff)


class PhyElecB_TitleScene(Scene):
    def construct(self):
        self.add(txtwatermark())
        txt = Text("【物理】通电螺线管与右手螺旋定则", t2c = { "【物理】": BLUE }).scale(1.4)
        self.play(DrawBorderThenFill(txt))
        self.wait()
        self.play(FadeOut(txt))

class PhyElecB_CurveScene(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(theta = 10 * DEGREES, phi = 70 * DEGREES)
        def frame_updater(frame, dt):
            frame.increment_theta(DEGREES * dt)
        frame.add_updater(frame_updater)
        
        self.add(txtwatermark().fix_in_frame())

        r_curve = RCurve(height = 6, w = 10.5, step_size = DEGREES * 2, color = GOLD)\
            .apply_depth_test().rotate(90 * DEGREES, axis = UP).rotate(-90 * DEGREES, axis = LEFT).shift(OUT)
        self.play(ShowCreation(r_curve))

        txt1 = Text("这是一个由导线绕成的螺线", t2c = { "螺线": BLUE }).scale(0.8).to_edge(DOWN).fix_in_frame()
        txt2 = Text("将其接入电路中", t2c = { "电路": BLUE }).scale(0.8).to_edge(DOWN).fix_in_frame()
        txt3 = Text("电流方向如图所示", t2c = { "电流方向": RED }).scale(0.6).to_edge(DOWN).fix_in_frame()
        battery = Battery().apply_depth_test().shift(IN * 2)
        linePo, lineNe = VMobject().apply_depth_test(), VMobject().apply_depth_test()
        linePo.set_points((r_curve.get_end(), r_curve.get_right() + IN * 3, battery.linePo.get_center()))
        lineNe.set_points((r_curve.get_start(), r_curve.get_left() + IN * 3, battery.lineNe.get_center()))
        linePo.insert_n_curves(8), lineNe.insert_n_curves(8)
        iLine = VMobject(color = RED, stroke_width = 6)
        iLine.set_points([
            *linePo.get_points()[::-1], *r_curve.get_points()[::-1], *lineNe.get_points()
            ])
        # arrows = VGroup()
        # for i in range(1, 11):
            
        self.play(Write(txt1))
        self.wait(1.5)
        self.play(FadeOut(txt1, run_time = 0.3), Write(txt2))
        self.play(*map(ShowCreation, (battery, linePo, lineNe)))
        self.play(txt2.animate.next_to(txt3, UP), FadeIn(txt3, UP))
        self.play(ShowPassingFlash(iLine), run_time = 3)

