import sys
sys.path.append(".")
import header as h
from manimlib import *

class Ybkc(VGroup):
    def __init__(self):
        def vertex_scale(v):
            for i in range(0, len(v)):
                    v[i] /= 4
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
            [-1.4, 0.4, 0],
            [-1.4, 0.85, 0],
            [-0.8, 3, 0]
        ]
        poly_back_curve = VMobject()
        poly_back_curve.set_points_as_corners(array_scale(poly_back_vertexs))
        poly_back_curve.data["points"][-2] = vertex_scale([-1.4, 2.1, 0])

        poly_back_curve.set_fill("#777777", opacity = 1).set_stroke(opacity = 0)
        self.back = poly_back_curve
        
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

        # slider (up)
        poly_slider_up_vertexs = [
            [0.1, 1.35, 0],
            [5.5, 1.35, 0],
            [5.5, 0.4, 0],
            [0.1, 0.4, 0],
            [0.1, 1.35, 0]
        ]
        poly_slider_up_curve = VMobject()
        poly_slider_up_curve.set_points_as_corners(array_scale(poly_slider_up_vertexs))
        poly_slider_up_curve.set_fill("#bbbbbb", opacity = 1).set_stroke(opacity = 0)
        self.poly_slider_up = poly_slider_up_curve

        # slider (down)
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
            [5.1, -1.35, 0]
        ]
        poly_slider_down_curve = VMobject()
        poly_slider_down_curve.set_points_as_corners(array_scale(poly_slider_down_vertexs))
        poly_slider_down_curve.set_fill("#bbbbbb", opacity = 1).set_stroke(opacity = 0)
        self.poly_slider_down = poly_slider_down_curve
        
        super().__init__(self.back, self.body, self.poly_slider_up, self.poly_slider_down)
    
    def sliders(self):
        return [self.back, self.poly_slider_up, self.poly_slider_down]

class Test(Scene):
    def construct(self):
        ybkc = Ybkc()
        self.play(FadeIn(ybkc, UP))
        # self.play(*[mobj.animate.shift(RIGHT * 2) for mobj in ybkc.sliders()])
