import sys
sys.path.append(".")
import header as h
from manimlib import *
import math as m

scale = 0.4

class Ybkc(Group):
    def __init__(self, **kwargs):
        # back
        poly_back_vertexs = np.array([
            np.array([-0.8, 3, 0]),
            np.array([-0.8, 1.35, 0]),
            np.array([0.1, 1.35, 0]),
            np.array([0.1, 0.4, 0]),
            np.array([-1.45, 0.4, 0]),
            np.array([-1.45, 0.85, 0]),
            np.array([-0.8, 3, 0])
        ]) * scale
        poly_back_curve = VMobject(plot_depth = -1)
        poly_back_curve.set_points_as_corners(poly_back_vertexs)
        poly_back_curve.data["points"][-2] = np.array([-1.45, 2.1, 0]) * scale
        poly_back_curve.set_fill("#aaaaaa", opacity = 1).set_stroke(width = 1)
        self.back = poly_back_curve

        # rdepth
        poly_rdepth_vertexs = np.array([
            np.array([0, 0.1, 0]),
            np.array([22.15, 0.1, 0]),
            np.array([22.15, -0.1, 0]),
            np.array([0, -0.1, 0])
        ]) * scale
        poly_rdepth_curve = VMobject(plot_depth = -1)
        poly_rdepth_curve.set_points_as_corners(poly_rdepth_vertexs)
        poly_rdepth_curve.set_fill("#aaaaaa", opacity = 1).set_stroke(width = 1)
        self.rdepth = poly_rdepth_curve
        
        # body
        poly_vertexs = np.array([
            np.array([-0.8, 3, 0]),
            np.array([-0.8, 1.25, 0]),
            np.array([-1.45, 1.25, 0]),
            np.array([-1.45, -1.5, 0]),
            np.array([-0.85, -4, 0]),
            np.array([0, -5, 0]),
            np.array([0, -2, 0]),
            np.array([-0.1, -1.9, 0]),
            np.array([-0.1, -0.85, 0]),
            np.array([22.15, -0.85, 0]),
            np.array([22.15, 0.85, 0]),
            np.array([0, 0.85, 0]),
            np.array([-0.8, 3, 0])
        ]) * scale
        poly_curve = VMobject()
        poly_curve.set_points_as_corners(poly_vertexs)
        poly_curve.data["points"][-2] = np.array([0, 2.1, 0]) * scale
        poly_curve.set_fill("#bbbbbb", opacity = 1).set_stroke(width = 1)
        poly_body_grads = Group()
        poly_body_numbers = Group()
        for i in range(0, 201):
            x = (0.3 + i * 0.1) * scale
            y = (-0.08 if i % 10 == 0 else (-0.17 if i % 5 == 0 else -0.26)) * scale
            poly_body_grads.add(Line([x, -0.65 * scale, 0], [x, y, 0], color = GREY_D).set_stroke(width = 0.35))
            if i % 10 == 0:
                number = Text(str(int(i / 10)), color = "#727272", font = "Noto Sans Thin")\
                    .scale(scale * 0.8).next_to([x, 0, 0], UP, 0.06 * scale).set_stroke(width = 0)
                poly_body_numbers.add(number)
        self.body_grads = poly_body_grads
        self.body = Group(poly_curve, poly_body_grads, poly_body_numbers, plot_depth = 0)

        # lmt
        lmt1 = Rectangle(0.8 * scale, 0.45 * scale, plot_depth = 1).move_to(np.array([2.45, 1.825, 0]) * scale)
        lmt1.set_fill("#cccccc", opacity = 1).set_stroke(width = 1)
        lmt2 = Rectangle(0.4 * scale, 0.25 * scale, plot_depth = 0).move_to(np.array([2.45, 1.475, 0]) * scale)
        lmt2.set_fill("#bdbdbd", opacity = 1).set_stroke(width = 1)
        self.lmt = Group(lmt1, lmt2, plot_depth = 0)

        # slider (up)
        poly_slider_up = Rectangle(5.4 * scale, 0.95 * scale, plot_depth = 1).move_to(np.array([2.8, 0.875, 0]) * scale)
        poly_slider_up.set_fill("#cccccc", opacity = 1).set_stroke(width = 1)
        self.slider_up = poly_slider_up

        # slider (down)
        psd_circle = Arc(start_angle = PI, angle = PI, radius = 0.45 * scale)\
            .next_to(np.array([4.65, -1.35, 0]) * scale, DOWN, 0).set_fill("#bbbbbb", opacity = 1).set_stroke(WHITE, 1)
        poly_slider_down_vertexs = np.array([
            np.array([4.2, -1.35, 0]),
            np.array([1.35, -1.35, 0]),
            np.array([0.85, -4, 0]),
            np.array([0, -5, 0]),
            np.array([0, -2, 0]),
            np.array([0.1, -1.9, 0]),
            np.array([0.1, -0.4, 0]),
            np.array([5.5, -0.4, 0]),
            np.array([5.5, -1.35, 0]),
            np.array([4.2, -1.35, 0])
        ]) * scale
        poly_slider_down_curve = VMobject()
        poly_slider_down_curve.set_points_as_corners(poly_slider_down_vertexs)
        poly_slider_down_curve.set_fill("#cccccc", opacity = 1).set_stroke(width = 1, background = False)
        psd_grads = Group()
        psd_numbers = Group()
        for i in range(0, 11):
            x = (0.3 + i * 0.09) * scale
            y = (-0.75 if i % 5 == 0 else -0.6) * scale
            psd_grads.add(Line([x, -0.425 * scale, 0], [x, y, 0], color = "#525252").set_stroke(width = 0.35))
            if i % 5 == 0:
                number = Text(str(i % 10), color = "#7a7a7a", font = "Noto Sans Thin")\
                    .scale(scale * 0.57).next_to([x, y, 0], DOWN, 0.05 * scale).set_stroke(width = 0)
                psd_numbers.add(number)
        psd_txt = Text("0 . 1 mm", color = "#7a7a7a", font = "Noto Sans Thin")\
            .scale(scale * 0.57).next_to(np.array([2.8, -0.875, 0]) * scale, RIGHT, 0).set_stroke(width = 0)
        self.sd_grads, self.sd_numbers, self.sd_txt = psd_grads, psd_numbers, psd_txt
        self.slider_down = Group(psd_circle, poly_slider_down_curve, psd_grads, psd_numbers, psd_txt, plot_depth = 1)
        
        super().__init__(self.back, self.rdepth, self.body, self.lmt, self.slider_up, self.slider_down, **kwargs)
    
    def sliders(self):
        return [self.back, self.rdepth, self.lmt, self.slider_up, self.slider_down]
    
    def in_animate(self):
        return AnimationGroup(
            FadeIn(self.back, LEFT), FadeIn(self.body, RIGHT),
            FadeIn(self.lmt, LEFT), FadeIn(self.slider_up, LEFT), FadeIn(self.slider_down, LEFT)
            )
    
    def out_animate(self):
        return AnimationGroup(
            FadeOut(self.back, RIGHT), FadeOut(self.body, LEFT),
            FadeOut(self.lmt, RIGHT), FadeOut(self.slider_up, RIGHT), FadeOut(self.slider_down, RIGHT)
            )
    
    # def scale(self, scale_factor, min_scale_factor=1e-8, about_point=None, about_edge=ORIGIN):
    #     self.orig_scale *= max(scale_factor, min_scale_factor)
    #     super().scale(scale_factor, min_scale_factor, about_point, about_edge)

class Lxcwq(Group):
    class GradLine(Line):
        def update_grad_pos(self, rot, x, y, y_radius):
            rot %= m.tau
            if rot >= m.pi * 0.5 and rot <= m.pi * 1.5:
                self.set_opacity(0)
            else:
                self.set_opacity(1)
                self.move_to([x, y - y_radius * m.sin(rot), 0])
            return self

    def __init__(self, **kwargs):
        self.rot = ValueTracker(0)

        # block
        block = VMobject(plot_depth = -101)
        block.set_points_as_corners(np.array([
            np.array([-1.5, 0.4, 0]),
            np.array([-1.4, 0.4, 0]),
            np.array([-1.4, -0.4, 0]),
            np.array([-1.5, -0.4, 0]),
            np.array([-1.5, 0.4, 0])
            ]) * scale)
        block.set_fill("#a4a4a4", opacity = 1).set_stroke(width = 1)

        # bar
        self.bar = bar = VMobject(plot_depth = -102)
        bar.set_points_as_corners(np.array([
            np.array([-1.4, 0.4, 0]),
            np.array([-1.4, -0.4, 0]),
            np.array([2, -0.4, 0]),
            np.array([2, 0.4, 0]),
            np.array([-1.4, 0.4, 0])
            ]) * scale)
        bar.set_fill("#aaaaaa", opacity = 1).set_stroke(width = 1)

        # backbody
        backbody = VMobject(plot_depth = -101)
        backbody.set_points_as_corners(np.array([
            np.array([3, 0.8, 0]),
            np.array([6, 0.8, 0]),
            np.array([6, -0.8, 0]),
            np.array([3, -0.8, 0])
            ]) * scale)
        backbody.set_fill("#bbbbbb", opacity = 1).set_stroke(width = 1)
        backbody_line = Line([3 * scale, 0, 0], [6 * scale, 0, 0], color = GREY_D, plot_depth = -100).set_stroke(width = 0.35)
        self.backbody_grad = backbody_grad = Group(plot_depth = -100)
        

        # body
        body = VMobject(plot_depth = -100)
        body.set_points((Arc.create_quadratic_bezier_points(-PI) * 3 + [0, -1.5, 0]) * scale)
        body.add_points_as_corners(np.array([
            np.array([-3, -1.5, 0]),
            np.array([-3, -1.4, 0])
            ]) * scale)
        body.append_points(np.array([
            np.array([-3, -1.4, 0]), 
            np.array([-2.5, -0.8, 0]), 
            np.array([-2.5, 0, 0])
            ]) * scale)
        body.add_points_as_corners(np.array([
            np.array([-2.5, 0, 0]),
            np.array([-2.5, 0.6, 0]),
            np.array([-1.5, 0.6, 0]),
            np.array([-1.5, -1.5, 0])
            ]) * scale)
        body.append_points((Arc.create_quadratic_bezier_points(PI, PI) * [1, 0.9, 0] * 1.5 + [0, -1.5, 0]) * scale)
        body.add_points_as_corners(np.array([
            np.array([1.5, -1.5, 0]),
            np.array([1.5, 1, 0]),
            np.array([3.25, 1, 0]),
            np.array([3.25, -1, 0]),
            np.array([3, -1.5, 0])
            ]) * scale)
        body.set_fill("#bbbbbb", opacity = 1).set_stroke(width = 1)

        # surf
        surf = VMobject(plot_depth = -99)
        surf.set_points((Arc.create_quadratic_bezier_points(PI, PI) * 2.8 + [0, -1.5, 0]) * scale)
        surf.add_points_as_corners(np.array([
            np.array([2.8, -1.5, 0]),
            np.array([1.7, -1.5, 0])
        ]) * scale)
        surf.append_points((Arc.create_quadratic_bezier_points(-PI) * [1, 0.9, 0] * 1.7 + [0, -1.5, 0]) * scale)
        surf.add_points_as_corners(np.array([
            np.array([-1.7, -1.5, 0]),
            np.array([-2.8, -1.5, 0])
        ]) * scale)
        surf.set_fill("#d0d0d0", opacity = 1).set_stroke(width = 1)

        # fixer
        fixer1 = VMobject(plot_depth = -100)
        fixer1.set_points_as_corners(np.array([
            np.array([8.5, 0.55, 0]),
            np.array([8.8, 0.55, 0]),
            np.array([8.8, -0.55, 0]),
            np.array([8.5, -0.55, 0]),
            np.array([8.5, 0.55, 0])
            ]) * scale)
        fixer1.set_fill("#bbbbbb", opacity = 1).set_stroke(width = 1)
        fixer2 = VMobject(plot_depth = -99)
        fixer2.set_points_as_corners(np.array([
            np.array([8.8, 0.6, 0]),
            np.array([10.35, 0.6, 0]),
            np.array([10.4, 0.55, 0]),
            np.array([10.4, -0.55, 0]),
            np.array([10.35, -0.6, 0]),
            np.array([8.8, -0.6, 0]),
            np.array([8.8, 0.6, 0])
            ]) * scale)
        fixer2.set_fill("#d0d0d0", opacity = 1).set_stroke(width = 1)
        fixer3 = VMobject(plot_depth = -98)
        fixer3.set_points_as_corners(np.array([
            np.array([9, 0.63, 0]),
            np.array([9.02, 0.65, 0]),
            np.array([10.08, 0.65, 0]),
            np.array([10.1, 0.63, 0]),
            np.array([10.1, -0.63, 0]),
            np.array([10.08, -0.65, 0]),
            np.array([9.02, -0.65, 0]),
            np.array([9, -0.63, 0]),
            np.array([9, 0.63, 0])
            ]) * scale)
        fixer3.set_fill("#c0c0d0", opacity = 1).set_stroke(width = 1)
        fixer_whorl = Group(plot_depth = -90)
        def fixer_whorl_updater(i):
            return lambda mobj, dt: mobj.update_grad_pos(
                self.rot.get_value() - m.tau / 25 * i,
                *fixer3.get_center()[0:2], fixer3.get_height() / 2
            ).set_stroke(width = 14 * m.cos(self.rot.get_value() - m.tau / 25 * i))
        for i in range(0, 25):
            whorl = self.GradLine(
                np.array([9, 0, 0]) * scale, np.array([10.1, 0, 0]) * scale,
                color = rgb_to_color(color_to_rgb("#c0c0ca") * 0.96), buff = 0.005, plot_depth = -90
                ).set_stroke(width = 14)
            whorl.add_updater(fixer_whorl_updater(i))
            fixer_whorl.add(whorl)
        fixer = Group(fixer1, fixer2, fixer3)

        # slider
        slider1 = VMobject(plot_depth = -99)
        slider1.set_points_as_corners(np.array([
            np.array([3.45, 0.85, 0]),
            np.array([8.4, 0.85, 0]),
            np.array([8.5, 0.65, 0]),
            np.array([8.5, -0.65, 0]),
            np.array([8.4, -0.85, 0]),
            np.array([3.45, -0.85, 0]),
            np.array([3.45, 0.85, 0])
            ]) * scale)
        # slider1.set_fill("#d0d0d0", opacity = 1).set_color_by_gradient(["#d0d0d0", "#d0d0d0", "#d0d0d0", "#848484", "#848484", "#848484"]).set_stroke(WHITE, width = 1)
        slider1.set_fill("#d0d0d0", opacity = 1).set_stroke(width = 1)
        slider2 = VMobject(plot_depth = -98)
        slider2.set_points_as_corners(np.array([
            np.array([5.9, 0.88, 0]),
            np.array([5.92, 0.9, 0]),
            np.array([8.28, 0.9, 0]),
            np.array([8.3, 0.88, 0]),
            np.array([8.3, -0.88, 0]),
            np.array([8.28, -0.9, 0]),
            np.array([5.92, -0.9, 0]),
            np.array([5.9, -0.88, 0]),
            np.array([5.9, 0.88, 0])
            ]) * scale)
        # slider2.set_fill("#c0c0ca", opacity = 1).set_color_by_gradient(["#c0c0ca", "#c0c0ca", "#c0c0ca", "#c0c0ca", "#7a7a80", "#7a7a80", "#7a7a80", "#c0c0ca"]).set_stroke(WHITE, width = 1)
        slider2.set_fill("#c0c0ca", opacity = 1).set_stroke(width = 1)
        self.slider_grad = slider_grad = Group(plot_depth = -90)
        def slider_grad_updater(i):
            return lambda mobj, dt: mobj.update_grad_pos(
                self.rot.get_value() - m.tau / 50 * i, 
                slider1.get_left()[0] + mobj.get_width() / 2, slider1.get_left()[1], slider1.get_height() / 2
                )
        for i in range(0, 50):
            grad = self.GradLine(
                np.array([3.47, 0, 0]) * scale, np.array([4.2 if i % 5 == 0 else 3.85, 0, 0]) * scale, 
                color = GREY_D, plot_depth = -90
                ).set_stroke(width = 0.35)
            grad.add_updater(slider_grad_updater(i))
            slider_grad.add(grad)
        slider_whorl = Group(plot_depth = -90)
        def slider_whorl_updater(i):
            return lambda mobj, dt: mobj.update_grad_pos(
                self.rot.get_value() - m.tau / 25 * i,
                *slider2.get_center()[0:2], slider2.get_height() / 2
            ).set_stroke(
                # rgb_to_color(color_to_rgb("#b6b6c0") * (-m.sin(self.rot.get_value() - m.tau / 25 * i) * 0.2 + 0.8)), 
                width = 17 * m.cos(self.rot.get_value() - m.tau / 25 * i)
            )
        for i in range(0, 25):
            whorl = self.GradLine(
                np.array([5.9, 0, 0]) * scale, np.array([8.3, 0, 0]) * scale,
                color = rgb_to_color(color_to_rgb("#c0c0ca") * 0.96), buff = 0.005, plot_depth = -90
                ).set_stroke(width = 17)
            whorl.add_updater(slider_whorl_updater(i))
            slider_whorl.add(whorl)
        self.slider = slider = Group(slider1, slider2)
        # self.slider = slider = Group(slider1, slider_grad)

        super().__init__(
            block, bar, 
            backbody, backbody_line, backbody_grad, 
            body, surf, fixer, 
            slider, slider_grad, slider_whorl, fixer_whorl, 
            **kwargs
            )

class YbkcScene(Scene):
    def construct(self):
        self.add(h.txtwatermark().set_plot_depth(-20000))

        imgYbkcLxcwq = ImageMobject("assets/ybkc_lxcwq.png", height = 7)
        txtYbkc = Text("游标卡尺").move_to(UP * 0.5)
        txtLxcwq = Text("螺旋测微器").move_to(DOWN * 2.6)
        Group(imgYbkcLxcwq, txtYbkc, txtLxcwq).shift(UP * 0.5)
        lineYbkc = Line(txtYbkc.get_left(), txtYbkc.get_right(), color = RED).next_to(txtYbkc, DOWN, SMALL_BUFF)
        lineLxcwq = Line(txtLxcwq.get_left(), txtLxcwq.get_right(), color = RED).next_to(txtLxcwq, DOWN, SMALL_BUFF)
        self.play(FadeIn(imgYbkcLxcwq, UP), run_time = 1.6)
        self.wait(0.3)
        self.play(
            DrawBorderThenFill(txtYbkc), DrawBorderThenFill(txtLxcwq),
            GrowArrow(lineYbkc), GrowArrow(lineLxcwq)
            )
        self.wait()

        txtYbkc2 = txtYbkc.copy().to_corner(UP)
        lineYbkc2 = lineYbkc.copy().next_to(txtYbkc2, DOWN, SMALL_BUFF).shift(LEFT * 10)
        self.play(
            *[FadeOut(m) for m in [txtYbkc, txtLxcwq, imgYbkcLxcwq, lineLxcwq]],
            AnimationGroup(lineYbkc.animate.shift(10 * RIGHT), rate_func = rush_into),
            FadeIn(txtYbkc2, DOWN), AnimationGroup(lineYbkc2.animate.shift(RIGHT * 10), rate_func = rush_from),
            run_time = 1
            )
        self.wait(0.5)

        ybkc = Ybkc().shift(LEFT * 4)
        ybkc.add_mouse_press_listner(lambda a, b: print(self.mouse_point.get_location()))
        self.play(ybkc.in_animate())
        self.wait(0.5)
        self.play(*[m.animate.shift(RIGHT * 1.5) for m in ybkc.sliders()])
        self.wait(0.5)
        
        exp1 = h.Explain([[-4.31, 1.19, 0], [-2.81, 1.19, 0]], UP, h.Explain.mtxt("内测量爪"), plot_depth = 10000)
        exp2 = h.Explain([[-4, -2.01, 0], [-2.48, -2.01, 0]], DOWN * 0.8, h.Explain.mtxt("外测量爪"), plot_depth = 10000)
        exp3 = h.Explain(np.array([-1.51, 0.76, 0]), UP, h.Explain.mtxt("紧固螺钉"), plot_depth = 10000)
        exp4 = h.Explain(np.array([-1.58, -0.34, 0]), DOWN, h.Explain.mtxt("游标尺"), plot_depth = 10000)
        exp5 = h.Explain(np.array([1.03, -0.02, 0]), UP, h.Explain.mtxt("主尺"), plot_depth = 10000)
        exp6 = h.Explain(np.array([5.47, 0, 0]), UP, h.Explain.mtxt("深度尺"), plot_depth = 10000)
        self.play(*[ShowCreation(exp) for exp in [exp1, exp2, exp3, exp4, exp5, exp6]], run_time = 1.5)
        self.wait(2)
        self.play(*[Uncreate(exp) for exp in [exp1, exp2, exp3, exp4, exp5, exp6]], run_time = 1.5)
        
        txtYbkcHow = Text("测量", color = BLUE_A).scale(0.8).next_to(txtYbkc2, RIGHT, aligned_edge = DOWN)
        obj = Rectangle(1.1, 1.6).set_fill(YELLOW_D, opacity = 1).set_stroke(WHITE, 1).shift(DOWN * 1.2 + LEFT * 3.45)
        self.play(FadeIn(obj, UP), ybkc.animate.shift(UP * 0.6), FadeIn(txtYbkcHow, DOWN))
        self.wait()
        self.play(*[m.animate.shift(LEFT * 0.4) for m in ybkc.sliders()])
        self.play(Group(ybkc, obj).animate.shift(RIGHT * 4 + DOWN * 2).scale(2))

        txtLock = Text("确定位置后旋紧紧固螺钉以锁定位置", t2c = { "旋紧": GOLD, "紧固螺钉": BLUE })\
            .scale(0.8).next_to(ybkc.lmt, UR, MED_LARGE_BUFF)
        arrowLock = Arrow(ybkc.lmt.get_top() + UP * 1.5, ybkc.lmt.get_top()).set_color(YELLOW)
        self.play(Write(txtLock))
        arrowLock.add_updater(lambda m: m.next_to(ybkc.lmt, UP))
        self.play(GrowArrow(arrowLock), ybkc.lmt.animate.shift(DOWN * 0.15))
        arrowLock.clear_updaters()
        self.wait(0.8)
        self.play(FadeOut(txtLock), FadeOut(arrowLock))

        self.play(Group(ybkc, obj).animate.shift(RIGHT * 5 + DOWN * 0.5).scale(1.7))
        self.play(*[grad.animate.set_stroke(width = 1.2) for grad in [*ybkc.body_grads, *ybkc.sd_grads]], run_time = 0.6)

        txtMain = Text("首先读取主尺刻度", t2c = { "主尺": BLUE }, plot_depth = 10000)\
            .scale(0.8).to_edge(UL, LARGE_BUFF).shift(DOWN * 0.8).set_stroke(GREY_BROWN, 4, background = True)
        txtDgtMain = Text("2.5 cm", color = YELLOW).next_to(ybkc.body_grads[25], UP, SMALL_BUFF)\
            .set_stroke(GREY_BROWN, 4, background = True)
        txtDgtMain2 = Text("25 mm", color = YELLOW).next_to(ybkc.body_grads[25], UP, SMALL_BUFF)\
            .set_stroke(GREY_BROWN, 4, background = True)
        txtSlider = Text("接着读取游标尺刻度与主尺刻度重合处", t2c = { "游标尺": BLUE, "主尺": BLUE, "重合处": GOLD }, plot_depth = 10000)\
            .scale(0.8).next_to(txtMain, DOWN, aligned_edge = LEFT).set_stroke(GREY_BROWN, 4, background = True)
        txtDgtSlider = Text("5", color = YELLOW)\
            .set_stroke(GREY_BROWN, 4, background = True).next_to(ybkc.sd_grads[5], DOWN, SMALL_BUFF)
        txtSum = Text("+", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True).next_to(txtDgtMain2)
        txtMul = Text("x", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True).next_to(txtDgtSlider)
        txtPrec = Text("0.1 mm", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True).next_to(txtMul)
        txtGetResult = Text("得到最终结果", plot_depth = 10000).scale(0.8)\
            .next_to(txtSlider, DOWN, aligned_edge = LEFT).set_stroke(GREY_BROWN, 4, background = True)
        txtResult = Text("= 25.5 mm", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True)
        lineMain = ybkc.body_grads[25].copy().set_color(YELLOW).set_stroke(width = 3)
        lineSlider = Line(ybkc.body_grads[32].get_end(), ybkc.sd_grads[5].get_end()).set_color(YELLOW).set_stroke(width = 3)
        self.play(GrowArrow(lineMain), DrawBorderThenFill(txtMain))
        self.wait(0.5)
        self.play(Write(txtDgtMain))
        self.wait(0.5)
        self.play(ReplacementTransform(txtDgtMain, txtDgtMain2))
        self.wait()
        self.play(GrowArrow(lineSlider), DrawBorderThenFill(txtSlider))
        self.wait(0.5)
        self.play(Write(txtDgtSlider), DrawBorderThenFill(txtMul), FadeTransform(ybkc.sd_txt.copy(), txtPrec))
        self.wait()
        self.play(DrawBorderThenFill(txtGetResult))
        self.play(Write(txtSum), Group(txtDgtSlider, txtMul, txtPrec).animate.next_to(txtSum))
        self.wait(0.5)
        txtResult.next_to(txtPrec)
        self.play(Write(txtResult))
        self.wait(0.5)
        self.play(ShowCreationThenFadeAround(txtResult[2:9]))
        self.wait(1.5)

        rect = Rectangle(FRAME_WIDTH, FRAME_HEIGHT * 0.35, plot_depth = 20000).set_fill(BLACK, 0.7).set_stroke(width = 0).shift(LEFT * FRAME_WIDTH)
        txt = Text("内测量爪、深度尺读数同理", t2c = { "内测量爪": BLUE, "深度尺": BLUE }, plot_depth = 20000)\
            .set_stroke(BLACK, 4, background = True)
        self.play(rect.animate.shift(RIGHT * FRAME_WIDTH), Write(txt))
        self.wait(1.5)
        self.play(rect.animate.shift(RIGHT * FRAME_WIDTH), FadeOut(txt, run_time = 0.5))
        self.remove(rect)

        txtYbkcWhy = Text("原理", color = BLUE_A).move_to(txtYbkcHow)
        self.play(
            *[FadeOut(m) for m in [txtMain, txtDgtMain2, txtSlider, txtDgtSlider, txtSum, txtMul, txtPrec, txtGetResult, txtResult]],
            FadeOut(lineMain), FadeOut(lineSlider), ybkc.lmt.animate.shift(UP * 0.15 * 1.7),
            FadeOut(txtYbkcHow, DOWN), FadeIn(txtYbkcWhy, DOWN)
            )
        self.wait(0.5)
        self.play(FadeOut(obj, DOWN), *[m.animate.shift(LEFT * 1.1 * 3.4) for m in ybkc.sliders()])
        self.play(*[FadeOut(m, UP) for m in [txtYbkc2, lineYbkc2, txtYbkcWhy]], ybkc.animate.shift(RIGHT * 14 + UP * 0.5).scale(1.8))

        txtw1 = Text("在这个十分度(精度0.1mm)游标卡尺中", t2c = { "十分度": BLUE, "[6:15]": GOLD }, plot_depth = 10000)\
            .scale(0.8).to_edge(UL, LARGE_BUFF).shift(DOWN * 0.8).set_stroke(GREY_BROWN, 4, background = True)
        txtw2 = Text("游标尺的十个刻度，仅占主尺的九个刻度", t2c = { "游标尺": BLUE, "主尺": BLUE, "十": GOLD, "九": GOLD }, plot_depth = 10000)\
            .scale(0.8).next_to(txtw1, DOWN, aligned_edge = LEFT).set_stroke(GREY_BROWN, 4, background = True)
        txtw3 = Text("所以游标尺每个刻度间距只有0.9mm", t2c = { "刻度间距": BLUE, "0.9mm": GOLD }, plot_depth = 10000)\
            .scale(0.8).next_to(txtw2, DOWN, aligned_edge = LEFT).set_stroke(GREY_BROWN, 4, background = True)
        self.play(Write(txtw1))
        self.wait(0.5)
        self.play(Write(txtw2), Succession(*[m.animate.set_color(BLUE_D) for m in ybkc.sd_grads], run_time = 2.5))
        def animate_main_sd_grad(main, sd, **kwargs):
            line = Line(ybkc.body_grads[main].get_end(), ybkc.sd_grads[sd].get_end(), color = YELLOW, plot_depth = 10000)
            return Succession(GrowArrow(line), FadeOut(line), **kwargs)
        self.play(animate_main_sd_grad(0, 0), animate_main_sd_grad(9, 10))
        self.play(Write(txtw3))
        self.wait()
        
        def movtxt(txt):
            return Text("当游标尺移动0.{}mm时".format(txt), t2c = { "游标尺": BLUE, "0.{}mm".format(txt): GOLD })\
                .scale(0.8).next_to(txtw1.get_left(), buff = 0).set_stroke(GREY_BROWN, 4, background = True)
        def movtxt2(txt):
            return Text("游标尺刻度“{}”正好与主尺刻度重合".format(txt), t2c = { "游标尺": BLUE, "主尺": BLUE, "“{}”".format(txt): GOLD, "重合": GOLD })\
                .scale(0.8).next_to(txtw4, DOWN, aligned_edge = LEFT).set_stroke(GREY_BROWN, 4, background = True)
        txtw4 = movtxt("1")
        txtw5 = movtxt2("1")
        self.play(Write(txtw4), *[FadeOut(m) for m in [txtw1, txtw2, txtw3]])
        self.play(*[m.animate.shift(RIGHT * 0.01 * 2.448) for m in ybkc.sliders()], run_time = 0.3)
        self.play(Write(txtw5))
        self.bring_to_back(ybkc)
        self.play(animate_main_sd_grad(1, 1, run_time = 0.7))
        for i in range(2, 5):
            self.play(
                Transform(txtw4, movtxt(i)), Transform(txtw5, movtxt2(i)),
                *[m.animate.shift(RIGHT * 0.01 * 2.448) for m in ybkc.sliders()], run_time = 0.6
                )
            self.bring_to_back(ybkc)
            self.play(animate_main_sd_grad(i, i, run_time = 0.7))
            self.wait(0.2)
        self.wait(0.8)
        self.play(
            *[FadeOut(m, run_time = 0.5) for m in [txtw4, txtw5]], ybkc.animate.scale(0.5).shift(LEFT * 14 + DOWN),
            FadeIn(txtYbkc2), FadeIn(lineYbkc2)
            )
        self.wait()
        self.play(ybkc.animate.shift(DOWN * 8), rate_func = rush_into)

        # self.play(Group(ybkc, obj).animate.shift(RIGHT * 8.6 + DOWN * 2.4).scale(3.4))
        # self.play(*[grad.animate.set_stroke(width = 1.2) for grad in [*ybkc.body_grads, *ybkc.sd_grads]], run_time = 0.6)
        
        # lineMain = ybkc.body_grads[25].copy().set_color(YELLOW).set_stroke(width = 3)
        # self.play(GrowArrow(lineMain))


        # rect = Rectangle(FRAME_WIDTH, FRAME_HEIGHT)
        # btn = Button(rect, lambda m: print(self.mouse_point.get_location()))
        # self.add(btn)
        # while(True):
        #     self.wait()

        # ybkc = Ybkc().shift(LEFT * 4)
        # self.play(ybkc.in_animate())
        # self.wait(0.5)
        # self.play(*[mobj.animate.shift(RIGHT * 2) for mobj in ybkc.sliders()])
        
class LxcwqScene(Scene):
    def construct(self):
        self.add(h.txtwatermark().set_plot_depth(-20000))

        lxcwq = Lxcwq()
        self.add(lxcwq)
        self.play(lxcwq.animate.scale(4).shift(LEFT * 4 + DOWN))
        self.play(lxcwq.rot.increment_value, 8, run_time = 4)
        self.wait()
