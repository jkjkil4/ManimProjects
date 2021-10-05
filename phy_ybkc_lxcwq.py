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
            self.move_to([x, y - y_radius * m.sin(rot), 0])
            if rot >= m.pi * 0.5 and rot <= m.pi * 1.5:
                self.set_opacity(0)
            else:
                self.set_opacity(1)
            return self
    class Whorl(VMobject):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.set_stroke(width = 0)

        def update_whorl(self, rot, x, y, x_radius, y_radius):
            rot %= m.tau
            yy = y - y_radius * m.sin(rot)
            self.move_to([x, yy, 0])
            if rot >= m.pi * 0.5 and rot <= m.pi * 1.5:
                self.set_opacity(0)
            else:
                self.set_opacity(1)
            yoff = y_radius / 16 * m.cos(rot)
            self.set_points_as_corners([
                [x - x_radius, yy + yoff, 0], [x + x_radius, yy + yoff, 0],
                [x + x_radius, yy - yoff, 0], [x - x_radius, yy - yoff, 0],
                ]).close_path()
            return self
    class GradNumber(Text):
        def update_grad_pos(self, rot, mobj):
            rot %= m.tau
            rot -= m.pi
            self.next_to(mobj, buff = 0)
            self.set_opacity(1 - max(0, 1 - max(0, abs(rot) - m.pi * 2 / 3) / (m.pi / 4)))
    
    @staticmethod
    def mm2rot(mm):
        return mm / 0.5 * m.tau
    @staticmethod
    def rot2mm(rot):
        return rot / m.tau * 0.5
    @staticmethod
    def grad2rot(grad):
        return m.tau / 50 * grad
    @staticmethod
    def rot2grad(rot):
        return rot / m.tau * 50

    def __init__(self, **kwargs):
        self.rot = ValueTracker(0)
        self.fixer_rot = ValueTracker(0)

        # block
        self.block = block = VMobject(plot_depth = -101)
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
            np.array([3.45, -0.4, 0]),
            np.array([3.45, 0.4, 0]),
            np.array([-1.4, 0.4, 0])
            ]) * scale)
        bar.set_fill("#aaaaaa", opacity = 1).set_stroke(width = 1)

        # backbody
        backbody1 = VMobject(plot_depth = -101)
        backbody1.set_points_as_corners(np.array([
            np.array([3, 0.8, 0]),
            np.array([6, 0.8, 0]),
            np.array([6, -0.8, 0]),
            np.array([3, -0.8, 0])
            ]) * scale)
        backbody1.set_fill("#bbbbbb", opacity = 1).set_stroke(width = 1)
        self.backbody_line = backbody_line = Line([3 * scale, 0, 0], [6 * scale, 0, 0], color = GREY_D, plot_depth = -100).set_stroke(width = 0.8)
        self.backbody_grad = backbody_grad = Group(plot_depth = -100)
        self.backbody_grad2 = backbody_grad2 = Group(plot_depth = -100)
        self.backbody_number = backbody_number = Group(plot_depth = -100)
        for i in range(0, 20):
            x = 3.45 + 0.1 * i
            y = 0.36 if i % 5 == 0 else 0.22
            backbody_grad.add(Line(np.array([x, 0.05, 0]) * scale, np.array([x, y, 0]) * scale, color = GREY_D).set_stroke(width = 0.8))
            backbody_grad2.add(Line(np.array([x + 0.05, -0.05, 0]) * scale, np.array([x + 0.05, -0.25, 0]) * scale, color = GREY_D).set_stroke(width = 0.8))
            if i % 5 == 0:
                number = Text(str(i), color = "#7a7a7a", font = "Noto Sans Thin").scale(0.2).next_to(backbody_grad[i], UP, 0.02)
                backbody_number.add(number)
        backbody = Group(backbody1, backbody_line, backbody_grad, backbody_grad2, backbody_number, plot_depth = -101)

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
            return lambda mobj: mobj.update_whorl(
                self.rot.get_value() + self.fixer_rot.get_value() - m.tau / 10 * i,
                *fixer3.get_center()[0:2], fixer3.get_width() / 2.05, fixer3.get_height() / 2.03
                )
        for i in range(0, 10):
            whorl = self.Whorl(color = rgb_to_color(color_to_rgb("#c0c0ca") * 0.96), plot_depth = -90)
            whorl.add_updater(fixer_whorl_updater(i))
            fixer_whorl.add(whorl)
        self.fixer = fixer = Group(fixer1, fixer2, fixer3, fixer_whorl, plot_depth = -100)

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
        slider2.set_fill("#c0c0ca", opacity = 1).set_stroke(width = 1)
        self.slider_grad = slider_grad = Group(plot_depth = -90)
        def slider_grad_updater(i):
            return lambda mobj, dt: mobj.update_grad_pos(
                self.rot.get_value() - m.tau / 50 * i, 
                slider1.get_left()[0] + mobj.get_width() / 2, slider1.get_left()[1], slider1.get_height() / 2.03
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
            return lambda mobj: mobj.update_whorl(
                self.rot.get_value() - m.tau / 10 * i,
                *slider2.get_center()[0:2], slider2.get_width() / 2.05, slider2.get_height() / 2.03
                )
        for i in range(0, 10):
            whorl = self.Whorl(color = rgb_to_color(color_to_rgb("#c0c0ca") * 0.96), plot_depth = -90)
            whorl.add_updater(slider_whorl_updater(i))
            slider_whorl.add(whorl)
        self.slider_number = slider_number = Group(plot_depth = -90)
        def slider_number_updater(i):
            return lambda mobj, dt: mobj.update_grad_pos(self.rot.get_value() - m.tau / 50 * i, slider_grad[i])
        for i in range(0, 50, 5):
            number = self.GradNumber(str(i), color = "#7a7a7a", font = "Noto Sans Thin", plot_depth = -90).scale(0.2)
            number.add_updater(slider_number_updater(i))
            slider_number.add(number)
        self.slider = slider = Group(slider1, slider2, slider_whorl, slider_grad, slider_number, plot_depth = -99)

        # limit
        limit1 = VMobject(plot_depth = -90)
        limit1.set_points((Arc.create_quadratic_bezier_points(TAU) * 0.52 + [2.375, 0, 0]) * scale)
        limit1.set_fill("#dddddd", opacity = 1).set_stroke(width = 1)
        limit2 = VMobject(plot_depth = -89)
        limit2.set_points_as_corners((np.array([
            np.array([0.4, 0.2, 0]),
            np.array([1, 0.2, 0]),
            np.array([1, -0.2, 0]),
            np.array([0.4, -0.2, 0])
            ]) + [2.375, 0, 0]) * scale)
        limit2.set_fill("#dddddd", opacity = 1).set_stroke(width = 1)
        def jRotate(self, angle, axis = OUT, **kwargs):
            self.rotate(angle, axis, **kwargs, about_point = limit1.get_center())
        def jRotateAnim(self, angle, axis = OUT, **kwargs):
            return Rotating(self, angle, axis, **kwargs, about_point = limit1.get_center())
        limit2.jRotate, limit2.jRotateAnim = jRotate, jRotateAnim
        limit2.jRotate(limit2, -PI / 4)
        self.limit = limit = Group(limit1, limit2, plot_depth = -90)

        bar.add_updater(lambda mobj, dt: mobj.next_to(slider, LEFT, buff = 0))
        slider.add_updater(
            lambda mobj, dt: mobj.next_to([
                self.backbody_grad[0].get_x() + self.rot2mm(self.rot.get_value()) * self.mmlen(), 
                backbody_line.get_y(), 0
                ], buff = 0))
        fixer.add_updater(lambda mobj, dt: mobj.next_to(slider, buff = 0))

        self.txt1 = txt1 = Text("0.01mm", color = "#7a7a7a", font = "Noto Sans Thin").scale(0.8 * scale)
        self.txt2 = txt2 = Text("0 - 25mm", color = "#7a7a7a", font = "Noto Sans Thin").scale(0.8 * scale)
        Group(txt1, txt2).arrange(DOWN, buff = MED_SMALL_BUFF * scale).move_to([0, -3.65 * scale, 0])

        super().__init__(
            block, bar, backbody,
            body, surf, fixer, slider,
            limit, txt1, txt2,
            **kwargs
            )
    
    def mmlen(self):
        return self.backbody_grad[1].get_x() - self.backbody_grad[0].get_x()

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
        # ybkc.add_mouse_press_listner(lambda a, b: print(self.mouse_point.get_location()))
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
        txtDgtMain = Text("2.7 cm", color = YELLOW).next_to(ybkc.body_grads[27], UP, SMALL_BUFF)\
            .set_stroke(GREY_BROWN, 4, background = True)
        txtDgtMain2 = Text("27 mm", color = YELLOW).next_to(ybkc.body_grads[27], UP, SMALL_BUFF)\
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
        txtResult = Text("= 27.5 mm", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True)
        lineMain = ybkc.body_grads[27].copy().set_color(YELLOW).set_stroke(width = 3)
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
        txtw6 = Text("......").scale(0.8).next_to(txtw5, DOWN, aligned_edge = LEFT).set_stroke(GREY_BROWN, 4, background = True)
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
        self.wait(0.3)
        self.play(Write(txtw6))
        self.wait(0.8)
        self.play(
            *[FadeOut(m, run_time = 0.5) for m in [txtw4, txtw5, txtw6]], ybkc.animate.scale(0.5).shift(LEFT * 14 + DOWN),
            FadeIn(txtYbkc2), FadeIn(lineYbkc2)
            )
        self.wait()
        self.play(ybkc.animate.shift(DOWN * 8), rate_func = rush_into)

class LxcwqSubScene(Scene):
    def construct(self):
        lxcwq = Lxcwq().scale(3.6).shift(UP * 2 + RIGHT * 3)
        self.add(lxcwq)
        self.wait(0.5)
        self.play(ShowCreationThenFadeAround(lxcwq.txt1))
        self.wait(0.5)

class LxcwqScene(Scene):
    def construct(self):
        wm = h.txtwatermark().set_plot_depth(-20000)
        self.add(wm)

        txtYbkc = Text("游标卡尺").to_corner(UP)
        lineYbkc = Line(txtYbkc.get_left(), txtYbkc.get_right(), color = RED).next_to(txtYbkc, DOWN, SMALL_BUFF)
        self.add(txtYbkc, lineYbkc)

        txtLxcwq = Text("螺旋测微器").to_corner(UP)
        lineLxcwq = Line(txtLxcwq.get_left(), txtLxcwq.get_right(), color = RED)\
            .next_to(txtLxcwq, DOWN, SMALL_BUFF).shift(LEFT * 10)
        lxcwq = Lxcwq().scale(1.6).shift(LEFT * 2)
        lxcwq.rot.set_value(Lxcwq.mm2rot(10))
        self.add(lxcwq)
        self.update_frame()
        self.remove(lxcwq)
        self.play(
            lineYbkc.animate.shift(RIGHT * 10), lineLxcwq.animate.shift(RIGHT * 10),
            ReplacementTransform(txtYbkc, txtLxcwq), FadeIn(lxcwq, UP)
            )
        self.wait(0.5)

        explist = [
            h.Explain(np.array([-3.78, 0.4, 0]), UP, "测砧"),
            h.Explain(np.array([-2.96, 0.4, 0]), DOWN * 0.8, "测微螺杆"),
            h.Explain(np.array([-1.98, -1.8, 0]), RIGHT * 1.5, "尺架"),
            h.Explain(np.array([-1.35, 0.4, 0]), UP, "止动旋钮"),
            h.Explain(np.array([-0.35, 0.4, 0]), DOWN, "固定刻度"),
            h.Explain(np.array([0.36, 0.86, 0]), UP, "可动刻度"),
            h.Explain(np.array([2.34, 0.1, 0]), DOWN, "粗调旋钮"),
            h.Explain(np.array([3.88, 0.2, 0]), DOWN, "微调旋钮")
            ]
        self.play(*[ShowCreation(m) for m in explist])
        self.wait(3)
        self.play(*[Uncreate(m) for m in explist])

        txt1 = Text("由于螺旋测微器可测量至毫米千分位", t2c = { "[2:7]": BLUE, "0.01": GOLD, "千分位": GOLD, "cm": GOLD }).scale(0.8)
        txt2 = Text("因此也被称为千分尺", t2c = { "千分尺": BLUE }).scale(0.8)
        g1_2 = Group(txt1, txt2).arrange(DOWN).to_corner(DOWN)
        self.play(Write(txt1), run_time = 2)
        self.play(Write(txt2[:6]))
        self.play(DrawBorderThenFill(txt2[6:]))
        self.wait()

        obj = Rectangle(0.17, 2).set_fill(YELLOW_D, opacity = 1).set_stroke(WHITE, 1)\
            .next_to(lxcwq.block, buff = 0).shift(UP * 0.6)
        txtHow = Text("测量", color = BLUE_A).scale(0.8).next_to(txtLxcwq, RIGHT, aligned_edge = DOWN)
        txtL = Text("转动粗调旋钮", t2c = { "粗调旋钮": BLUE }).scale(0.8).to_corner(DOWN)
        txtM = Text("接近物体时，转动微调旋钮", t2c = { "接近": GOLD, "微调旋钮": BLUE }).scale(0.8)
        txtNotice = Text("(避免压力过大损坏螺旋测微器)", color = GREY).scale(0.6)
        Group(txtM, txtNotice).arrange(DOWN).to_corner(DOWN)
        offsetmm = Lxcwq.mm2rot((obj.get_right()[0] - lxcwq.bar.get_left()[0]) / lxcwq.mmlen())
        self.play(FadeOut(g1_2, DOWN), FadeIn(obj, DOWN), FadeIn(txtHow, DOWN))
        self.play(DrawBorderThenFill(txtL))
        self.play(FocusOn(lxcwq.slider[1]))
        self.play(lxcwq.rot.animate.increment_value(offsetmm * 0.8), run_time = 2)
        self.wait(0.5)
        txtM.save_state()
        txtM.to_corner(DOWN)
        self.play(ReplacementTransform(txtL, txtM))
        self.play(txtM.animate.restore(), FadeIn(txtNotice, UP), run_time = 0.8)
        self.play(FocusOn(lxcwq.fixer[1]))
        self.play(lxcwq.rot.animate.increment_value(offsetmm * 0.2), rate_func = rush_into)
        self.play(lxcwq.fixer_rot.animate.increment_value(-2.2), rate_func = rush_from, run_time = 0.6)
        self.wait()
        self.play(FadeOut(txtM, DOWN), FadeOut(txtNotice, DOWN))

        arrowLmt = Arrow([-0.6, 0, 0], [-1.53, 0, 0], buff = 0).set_color(YELLOW)
        txtLmt = Text("扣上止动旋钮以锁定位置", t2c = { "扣上": GOLD, "止动旋钮": BLUE })\
            .scale(0.8).next_to(arrowLmt, DOWN, aligned_edge = LEFT).set_stroke(GREY_BROWN, 4, background = True)
        self.play(Write(txtLmt))
        self.play(
            GrowArrow(arrowLmt, rate_func = rush_from, run_time = 1), 
            lxcwq.limit[1].jRotateAnim(lxcwq.limit, -PI / 2, rate_func = linear, run_time = 0.8)
            )
        self.wait(0.8)
        self.play(FadeOut(arrowLmt), FadeOut(txtLmt))

        self.play(Group(lxcwq, obj).animate.scale(3.8).shift(DOWN * 1.8 + LEFT * 1.5))
        # self.play(*[m.animate.set_stroke(width = 1.2) for m in [*lxcwq.backbody_grad, *lxcwq.backbody_grad2, *lxcwq.slider_grad]], run_time = 0.6)

        txtH1 = Text("首先读取固定刻度", t2c = { "固定刻度": BLUE })\
            .scale(0.8).to_edge(UR, 1.2).shift(DOWN * 0.6).set_stroke(GREY_BROWN, 4, background = True)
        self.play(Write(txtH1))
        self.wait(0.5)

        def gradArrow(index):
            grad: Line = lxcwq.backbody_grad[int(index / 2)] if index % 2 == 0 else lxcwq.backbody_grad2[int((index - 1) / 2)]
            y = grad.get_bottom()[1]
            return Arrow([grad.get_x(), y - 1, 0], [grad.get_x(), y, 0], buff = 0)\
                .set_fill(YELLOW).set_stroke(GREY_BROWN, 4, background = True)
        arrow = gradArrow(0)
        def gradNum(index):
            mobj = Text(str(int(index / 2) if index % 2 == 0 else index / 2) + " mm", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True)
            mobj.add_updater(lambda m: m.next_to(arrow, DOWN))
            return mobj
        num = gradNum(0)
        self.play(Write(num), Write(arrow))
        self.wait(0.5)
        for i in range(0, 5, 2):
            self.play(Transform(arrow, gradArrow(i)), Transform(num, gradNum(i)), run_time = 0.8)
            self.wait(0.5)
        self.play(Transform(arrow, gradArrow(5)), Transform(num, gradNum(5)))
        num.clear_updaters()
        self.wait(0.8)
        self.play(FadeOut(arrow), num.animate.shift(DOWN))

        txtH2 = Text("再读取可动刻度(估读)", t2c = { "可动刻度": BLUE, "估读": GOLD })\
            .scale(0.8).next_to(txtH1, DOWN, aligned_edge = RIGHT).set_stroke(GREY_BROWN, 4, background = True)
        self.play(Write(txtH2))
        self.wait(0.5)
        
        def sgradArrow(index):
            grad: Line = lxcwq.slider_grad[index]
            x = grad.get_left()[0]
            return Arrow([x - 1, grad.get_y(), 0], [x, grad.get_y(), 0], buff = 0)\
                .set_fill(YELLOW).set_stroke(GREY_BROWN, 4, background = True)
        sarrow = sgradArrow(15)
        def sgradNum(index):
            mobj = Text(str(index) if isinstance(index, int) else index, color = YELLOW)\
                .set_stroke(GREY_BROWN, 4, background = True)
            mobj.add_updater(lambda m: m.next_to(sarrow, LEFT))
            return mobj
        snum = sgradNum(15)
        self.play(Write(sarrow), Write(snum))
        self.wait(0.5)
        self.play(Transform(sarrow, sgradArrow(16)), Transform(snum, sgradNum(16)))
        self.wait(0.5)
        snum_target = sgradNum("(估读) 15.6")
        snum_target.set_color_by_t2c({ "估读": GOLD })
        snum_target.set_stroke(GREY_BROWN, 4, background = True)
        self.play(
            sarrow.animate.set_y(lxcwq.backbody_line.get_y()), 
            Transform(snum, snum_target)
            )
        self.wait(2)    # Insert LxcwqSubScene

        txtSnumCpy = snum[5:].copy()
        txtSum = Text("+", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True).next_to(num)
        txtMul = Text("x", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True).next_to(snum)
        txtPrec = Text("0.01 mm", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True).next_to(txtMul)
        txtResult = Text("= 2.656 mm", color = YELLOW).set_stroke(GREY_BROWN, 4, background = True)
        txtH3 = Text("得到最终结果").scale(0.8)\
            .next_to(txtH2, DOWN, aligned_edge = RIGHT).set_stroke(GREY_BROWN, 4, background = True)
        self.play(FadeOut(sarrow), DrawBorderThenFill(txtMul), Write(txtPrec))
        self.wait()
        self.play(DrawBorderThenFill(txtH3))
        self.play(FadeOut(snum), Group(txtSnumCpy, txtMul, txtPrec).animate.next_to(txtSum), DrawBorderThenFill(txtSum))
        self.wait(0.5)
        txtResult.next_to(txtPrec)
        self.play(Write(txtResult))
        self.play(ShowCreationThenFadeAround(txtResult[2:]))
        self.wait(1.5)

        txtWhy = Text("原理", color = BLUE_A).scale(0.8).move_to(txtHow)
        self.play(
            *[FadeOut(m) for m in [num, txtSum, txtSnumCpy, txtMul, txtPrec, txtResult, txtH1, txtH2, txtH3]],
            FadeOut(txtHow, DOWN), FadeIn(txtWhy, DOWN),
            lxcwq.limit[1].jRotateAnim(lxcwq.limit, PI / 2),
            run_time = 1)
        self.play(lxcwq.rot.animate.set_value(Lxcwq.mm2rot(1)), run_time = 2.5)

        txtW1 = Text("可动刻度每转一圈，固定刻度就会前进/后退0.5mm", t2c = { "可动刻度": BLUE, "一圈": GOLD, "固定刻度": BLUE, "0.5mm": GOLD })\
            .scale(0.8).to_edge(UR, 1.2).shift(DOWN * 0.6).set_stroke(GREY_BROWN, 4, background = True)
        txtW2 = Text("同时，可动刻度被分成了50个刻度", t2c = { "可动刻度": BLUE, "50": GOLD })\
            .scale(0.8).next_to(txtW1, DOWN, aligned_edge = RIGHT).set_stroke(GREY_BROWN, 4, background = True)
        txtW3 = Text("也就是每个刻度对应")\
            .scale(0.8).next_to(txtW2, DOWN, aligned_edge = RIGHT).set_stroke(GREY_BROWN, 4, background = True)
        txtW4_1 = Tex("\\frac{0.5mm}{50}", color = GOLD)\
            .scale(0.8).next_to(txtW3, DOWN).set_stroke(GREY_BROWN, 4, background = True)
        txtW4_2 = Tex("0.01mm", color = GOLD)\
            .scale(0.8).next_to(txtW3, DOWN).set_stroke(GREY_BROWN, 4, background = True)
        txtW5 = Text("这样就可以通过读取固定刻度和可动刻度来测量长度", t2c = { "固定刻度": BLUE, "可动刻度": BLUE, "测量长度": GOLD })\
            .scale(0.8).next_to(txtW4_2, DOWN).to_corner(RIGHT, 1.2).set_stroke(GREY_BROWN, 4, background = True)
        self.play(Write(txtW1))
        self.play(lxcwq.rot.animate.increment_value(Lxcwq.mm2rot(-0.5)), run_time = 1.5)
        self.wait(0.5)
        self.play(Write(txtW2))
        self.play(Succession(*[m.animate.set_color(YELLOW) for m in lxcwq.slider_grad if m.get_opacity() != 0], lag_ratio = 0.01))
        self.wait(0.5)
        self.play(Succession(*[m.animate.set_color(GREY_D) for m in lxcwq.slider_grad if m.get_opacity() != 0], lag_ratio = 0.01))
        self.wait(0.5)
        self.play(Write(txtW3))
        self.wait(0.5)
        self.play(DrawBorderThenFill(txtW4_1))
        self.wait(0.5)
        self.play(Transform(txtW4_1, txtW4_2))
        self.wait()
        self.play(Write(txtW5))
        self.wait(2)

        # lxcwq.add_mouse_press_listner(lambda a, b: print(self.mouse_point.get_location()))
        # while(True):
        #     self.wait(10)
        
