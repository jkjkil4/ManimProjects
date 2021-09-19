import sys
sys.path.append(".")
import header as h
from manimlib import *
import math as m

class Ybkc(VGroup):
    def __init__(self):
        scale = 0.4

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
        poly_back_curve.set_fill("#828282", opacity = 1).set_stroke(width = 1)
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
        poly_rdepth_curve.set_fill("#858585", opacity = 1).set_stroke(width = 1)
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
        poly_curve.set_fill("#999999", opacity = 1).set_stroke(width = 1)
        poly_body_grads = VGroup()
        poly_body_numbers = VGroup()
        for i in range(0, 201):
            x = (0.3 + i * 0.1) * scale
            y = (-0.08 if i % 10 == 0 else (-0.17 if i % 5 == 0 else -0.26)) * scale
            poly_body_grads.add(Line([x, -0.65 * scale, 0], [x, y, 0], color = GREY_D).set_stroke(width = 0.35))
            if i % 10 == 0:
                number = Text(str(int(i / 10)), color = "#727272", font = "Noto Sans Thin")\
                    .scale(scale * 0.8).next_to([x, 0, 0], UP, 0.06 * scale).set_stroke(width = 0)
                poly_body_numbers.add(number)
        self.body = VGroup(poly_curve, poly_body_grads, poly_body_numbers)

        # lmt
        lmt1 = Rectangle(0.8 * scale, 0.45 * scale, plot_depth = 1).move_to(np.array([2.45, 1.825, 0]) * scale)
        lmt1.set_fill("#adadad", opacity = 1).set_stroke(width = 1)
        lmt2 = Rectangle(0.4 * scale, 0.25 * scale, plot_depth = 0).move_to(np.array([2.45, 1.475, 0]) * scale)
        lmt2.set_fill("#a0a0a0", opacity = 1).set_stroke(width = 1)
        self.lmt = VGroup(lmt1, lmt2)

        # slider (up)
        poly_slider_up = Rectangle(5.4 * scale, 0.95 * scale, plot_depth = 1).move_to(np.array([2.8, 0.875, 0]) * scale)
        poly_slider_up.set_fill("#a4a4a4", opacity = 1).set_stroke(width = 1)
        self.slider_up = poly_slider_up

        # slider (down)
        psd_circle = Arc(start_angle = PI, angle = PI, radius = 0.45 * scale)\
            .next_to(np.array([4.65, -1.35, 0]) * scale, DOWN, 0).set_fill("#999999", opacity = 1).set_stroke(WHITE, 1)
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
        poly_slider_down_curve.set_fill("#a7a7a7", opacity = 1).set_stroke(width = 1)
        psd_grads = VGroup()
        psd_numbers = VGroup()
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
        self.slider_down = VGroup(psd_circle, poly_slider_down_curve, psd_grads, psd_numbers, psd_txt, plot_depth = 1)
        
        super().__init__(self.back, self.rdepth, self.body, self.lmt, self.slider_up, self.slider_down)
    
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

class Test(Scene):
    def construct(self):
        ybkc = Ybkc().shift(LEFT * 4)
        self.play(ybkc.in_animate())
        self.wait(0.5)
        self.play(*[mobj.animate.shift(RIGHT * 2) for mobj in ybkc.sliders()])
        self.wait(0.5)
        self.play(*[mobj.animate.shift(LEFT * 2) for mobj in ybkc.sliders()])
        # self.wait(0.2)
        # self.remove(ybkc.rdepth)
        # self.play(ybkc.out_animate())
        
