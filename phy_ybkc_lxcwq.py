import sys
sys.path.append(".")
import header as h
from manimlib import *
import math as m

class Ybkc(VGroup):
    def __init__(self):
        def var_scale(v):
            return v / 4
        def vertex_scale(v):
            for i in range(0, len(v)):
                    v[i] = var_scale(v[i])
            return v
        def array_scale(a):
            for vertex in a:
                vertex_scale(vertex)
            return a

        # back
        poly_back_vertexs = [
            [-0.8, 3, 0],
            [-0.8, 1.35, 0],
            [0.1, 1.35, 0],
            [0.1, 0.4, 0],
            [-1.45, 0.4, 0],
            [-1.45, 0.85, 0],
            [-0.8, 3, 0]
        ]
        poly_back_curve = VMobject(plot_depth = -1)
        poly_back_curve.set_points_as_corners(array_scale(poly_back_vertexs))
        poly_back_curve.data["points"][-2] = vertex_scale([-1.45, 2.1, 0])
        poly_back_curve.set_fill("#828282", opacity = 1).set_stroke(opacity = 0)
        self.back = poly_back_curve

        # rdepth
        poly_rdepth_vertexs = [
            [0, 0.1, 0],
            [22.15, 0.1, 0],
            [22.15, -0.1, 0],
            [0, -0.1, 0]
        ]
        poly_rdepth_curve = VMobject(plot_depth = -1)
        poly_rdepth_curve.set_points_as_corners(array_scale(poly_rdepth_vertexs))
        poly_rdepth_curve.set_fill("#858585", opacity = 1).set_stroke(opacity = 0)
        self.rdepth = poly_rdepth_curve
        
        # body
        poly_vertexs = [
            [-0.8, 3, 0],
            [-0.8, 1.25, 0],
            [-1.45, 1.25, 0],
            [-1.45, -1.5, 0],
            [-0.85, -4, 0],
            [0, -5, 0],
            [0, -2, 0],
            [-0.1, -1.9, 0],
            [-0.1, -0.85, 0],
            [22.15, -0.85, 0],
            [22.15, 0.85, 0],
            [0, 0.85, 0],
            [-0.8, 3, 0]
        ]
        poly_curve = VMobject()
        poly_curve.set_points_as_corners(array_scale(poly_vertexs))
        poly_curve.data["points"][-2] = vertex_scale([0, 2.1, 0])
        poly_curve.set_fill("#999999", opacity = 1).set_stroke(opacity = 0)
        self.body = poly_curve

        # lmt
        lmt1 = Rectangle(var_scale(0.8), var_scale(0.45), plot_depth = 1).move_to(vertex_scale([2.45, 1.825, 0]))
        lmt1.set_fill("#bbbbbb", opacity = 1).set_stroke(opacity = 0)
        lmt2 = Rectangle(var_scale(0.4), var_scale(0.25), plot_depth = 0).move_to(vertex_scale([2.45, 1.475, 0]))
        lmt2.set_fill("#a4a4a4", opacity = 1).set_stroke(opacity = 0)
        self.lmt = VGroup(lmt1, lmt2)

        # slider (up)
        poly_slider_up = Rectangle(var_scale(5.4), var_scale(0.95), plot_depth = 1).move_to(vertex_scale([2.8, 0.875, 0]))
        poly_slider_up.set_fill("#bbbbbb", opacity = 1).set_stroke(opacity = 0)
        self.slider_up = poly_slider_up

        # slider (down)
        sqrt2 = m.sqrt(2)
        psd_cr_scale = 1.15
        poly_slider_down_vertexs = [
            [4.2, -1.35, 0],
            [1.35, -1.35, 0],
            [0.85, -4, 0],
            [0, -5, 0],
            [0, -2, 0],
            [0.1, -1.9, 0],
            [0.1, -0.4, 0],
            [5.5, -0.4, 0],
            [5.5, -1.35, 0],
            [5.1, -1.35, 0],
            [4.65 + 0.45 / sqrt2, -1.35 - 0.45 / sqrt2, 0],
            [4.65, -1.8, 0],
            [4.65 - 0.45 / sqrt2, -1.35 - 0.45 / sqrt2, 0],
            [4.2, -1.35, 0]
        ]
        poly_slider_down_curve = VMobject(plot_depth = 1)
        poly_slider_down_curve.set_points_as_corners(array_scale(poly_slider_down_vertexs))
        for point in poly_slider_down_curve.data["points"][-2:-12:-3]:
            point -= vertex_scale([4.65, -1.35, 0])
            point *= psd_cr_scale
            point += vertex_scale([4.65, -1.35, 0])
        poly_slider_down_curve.set_fill("#bbbbbb", opacity = 1).set_stroke(opacity = 0)
        self.slider_down = poly_slider_down_curve
        
        super().__init__(self.back, self.rdepth, self.body, self.lmt, self.slider_up, self.slider_down)
    
    def sliders(self):
        return [self.back, self.rdepth, self.lmt, self.slider_up, self.slider_down]
    
    def in_animate(self):
        return AnimationGroup(
            FadeIn(self.back, DOWN), FadeIn(self.body, RIGHT),
            FadeIn(self.lmt, DOWN), FadeIn(self.slider_up, DOWN), FadeIn(self.slider_down, UP)
            )
    
    def out_animate(self):
        return AnimationGroup(
            FadeOut(self.back, UP), FadeOut(self.body, LEFT),
            FadeOut(self.lmt, UP), FadeOut(self.slider_up, UP), FadeOut(self.slider_down, DOWN)
            )

class Test(Scene):
    def construct(self):
        ybkc = Ybkc().shift(LEFT * 2)
        self.play(ybkc.in_animate())
        self.wait(0.5)
        self.play(*[mobj.animate.shift(RIGHT * 2) for mobj in ybkc.sliders()])
        self.wait(0.5)
        self.play(*[mobj.animate.shift(LEFT * 2) for mobj in ybkc.sliders()])
        # self.wait(0.2)
        # self.remove(ybkc.rdepth)
        # self.play(ybkc.out_animate())
        
