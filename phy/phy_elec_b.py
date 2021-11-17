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

class BTip(VGroup):
    CONFIG = {
        "circle_radius": 0.4,
        "tip_radius": 0.2,
        "arrowtip_config": {}
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.circle = Circle(radius = self.circle_radius, fill_color = GREY_D, fill_opacity = 1, stroke_color = GREY_B, stroke_width = 4)
        tip1 = ArrowTip().set_color(RED).set_width(self.tip_radius)
        tip2 = tip1.copy().rotate(PI).set_color(BLUE)
        self.tips = VGroup(tip2, tip1).arrange(buff = 0)

        self.add(self.circle, self.tips)

class IncreaseArrow(Arrow):
    def __init__(self, mobj, nxt_buff = 0.2, **kwargs):
        if not "buff" in kwargs:
            kwargs["buff"] = 0
        if not "path_arc" in kwargs:
            kwargs["path_arc"] = 60 * DEGREES
        a = mobj.get_edge_center(DR) + nxt_buff * DR
        b = mobj.get_edge_center(UR) + nxt_buff * UR
        super().__init__(a, b, **kwargs)
        self.fix_in_frame()

def tangent_direction(mobj, alpha, d_alpha = 1e-6):
    a1 = clip(alpha - d_alpha, 0, 1)
    a2 = clip(alpha + d_alpha, 0, 1)
    return mobj.pfp(a2) - mobj.pfp(a1)

# class PhyElecB_TestScene(Scene):
#     def construct(self):
#         self.add(BTip())

class PhyElecB_TitleScene(Scene):
    def construct(self):
        self.add(txtwatermark())
        txt = Text("【物理】通电螺线管、直导线与右手螺旋定则", t2c = { "【物理】": BLUE }).scale(1.4)
        self.play(DrawBorderThenFill(txt))
        self.wait()
        self.play(FadeOut(txt))

class PhyElecB_CurveChapterScene(ChapterScene):
    CONFIG = {
        "str1": "Part 1",
        "str2": "通电螺线管"
    }

class PhyElecB_CurveScene(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(theta = 10 * DEGREES, phi = 70 * DEGREES)
        frame_theta_rate = 1
        def frame_updater(frame, dt):
            frame.increment_theta(DEGREES * dt * frame_theta_rate)
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
        arrows = VGroup()
        for i in range(19, 0, -2):
            k1 = (i + 1) / 21
            k2 = i / 21
            a = r_curve.get_left() * (1 - k1) + r_curve.get_right() * k1
            b = r_curve.get_left() * (1 - k2) + r_curve.get_right() * k2
            arrows.add(
                ArrowTip(width = 0.15).set_stroke(RED).set_fill(RED, 0.5).move_to(a + UP)\
                    .rotate(90 * DEGREES).rotate(-89 * DEGREES, axis = RIGHT)
                )
            arrows.add(
                ArrowTip(width = 0.15).set_stroke(RED).set_fill(RED, 1).move_to(b + DOWN)\
                    .rotate(90 * DEGREES).rotate(89 * DEGREES, axis = RIGHT)
                )
        self.play(Write(txt1))
        self.wait(1.5)
        self.play(FadeOut(txt1, run_time = 0.3), Write(txt2))
        self.play(*map(ShowCreation, (battery, linePo, lineNe)))
        self.play(txt2.animate.next_to(txt3, UP), FadeIn(txt3, UP))
        self.play(
            Succession(*[SucAbleFadeIn(arrows[i], IN if i % 2 == 0 else OUT) for i in range(len(arrows))], run_time = 2),
            ShowPassingFlash(iLine, run_time = 2.4)
            )
        self.wait(0.5)

        txt4 = Text("也就是说，电流沿该方向环绕", t2c = { "沿该方向环绕": GOLD }).scale(0.8).to_edge(DOWN).fix_in_frame()
        rotate_center = r_curve.get_center()
        rotate_points = (rotate_center + LEFT * 1.5, rotate_center + UP * 1.5, rotate_center + RIGHT * 1.5, rotate_center + DOWN * 1.5)
        rotate_arrows = VGroup()
        for i in range(len(rotate_points)):
            rotate_arrows.add(Arrow(rotate_points[i - 1], rotate_points[i], path_arc = -70 * DEGREES))
        rotate_arrows.set_color(RED).insert_n_curves(2).apply_depth_test().rotate(87 * DEGREES, axis = UP)
        try:
            self.play(
                *map(lambda m: FadeOut(m, run_time = 0.3), (txt2, txt3, arrows)), 
                Write(txt4), Write(rotate_arrows)
                )
        except:
            self.add(txt2, txt3, arrows, rotate_arrows)
        self.wait(0.5)
        frame.remove_updater(frame_updater)
        self.play(frame.animate.set_euler_angles(theta = 84 * DEGREES, phi = 86 * DEGREES), run_time = 1.6)
        self.wait()
        self.play(frame.animate.set_euler_angles(theta = 40 * DEGREES, phi = 65 * DEGREES), FadeOut(txt4, DOWN))
        frame_theta_rate = 0.5
        frame.add_updater(frame_updater)
        self.wait()

        txt5 = Text("想象用右手环绕螺线，且除拇指外四指方向与电流环绕方向一致", t2c = { "右手": BLUE, "环绕螺线": GOLD, "方向一致": GOLD })\
            .scale(0.8).to_edge(DOWN).fix_in_frame()
        txt6 = Text("则拇指伸出方向即为其中磁场方向", t2c = { "拇指伸出方向": BLUE, "磁场方向": PURPLE }).scale(0.7).to_edge(DOWN).fix_in_frame()
        bLine = Arrow(rotate_center + RIGHT * 5, rotate_center + LEFT * 5).set_color(PURPLE).apply_depth_test()
        self.play(Write(txt5), run_time = 2.5)
        self.wait(4)
        self.play(FadeIn(txt6, UP), txt5.animate.next_to(txt5, UP), GrowArrow(bLine))
        self.wait(1.5)
        frame.remove_updater(frame_updater)
        linePo.set_stroke(opacity = (1, 1))
        lineNe.set_stroke(opacity = (1, 1))
        frame_saved_width = frame.get_width()
        self.play(
            *map(FadeOut, (txt5, txt6, battery, rotate_arrows)),
            linePo.animate.set_stroke(opacity = (0.5, 0)), lineNe.animate.set_stroke(opacity = (0.5, 0)),
            frame.animate.set_euler_angles(theta = 0, phi = 0).set_width(frame.get_width() * 1.5), 
            run_time = 2)
        self.wait(0.5)
        
        c = Circle(color = PURPLE, stroke_width = 6).rotate(-PI / 2)\
            .reverse_points().next_to(rotate_center, UP, 0).stretch(4, 0).stretch(0.6, 1, about_point = rotate_center).shift(UP * 0.5)
        circles1 = VGroup(c)
        for i in range(1, 3):
            k = i / 3
            pos = rotate_center + UP * 0.5 * (1 - k)
            c = c.copy().stretch(3, 0).stretch(4, 1).next_to(pos, UP, 0)
            circles1.add(c)
        circles1.apply_depth_test().apply_complex_function(lambda z: (z.real * (1 / (z.imag + 2) + 0.5) + 1j * z.imag))
        arrowTips1 = VGroup()
        def get_tangent_arrows(mobj, vg):
            for i in range(0, 10):
                alpha = i / 10
                tangent = tangent_direction(mobj, alpha)
                angle = np.arctan2(tangent[1], tangent[0])
                vg.add(ArrowTip(width = 0.25, angle = angle).set_color(PURPLE).move_to(mobj.pfp(alpha) + OUT * 0.02))
        for circle in circles1:
            get_tangent_arrows(circle, arrowTips1)
        arrowTips1.apply_depth_test()
        circles2 = circles1.copy().stretch(-1, 1, about_point = rotate_center)
        arrowTips2 = VGroup()
        for circle in circles2:
            get_tangent_arrows(circle, arrowTips2)
        arrowTips2.apply_depth_test()
        lineCenter = Line(rotate_center + RIGHT * 16, rotate_center + LEFT * 16, color = PURPLE, stroke_width = 6)\
            .apply_depth_test()
        arrowTipsCenter = VGroup()
        get_tangent_arrows(lineCenter, arrowTipsCenter)
        arrowTipsCenter.apply_depth_test()
        self.play(*map(Write, (circles1, circles2, lineCenter)))
        self.remove(bLine)
        self.play(*map(Write, (arrowTips1, arrowTips2, arrowTipsCenter)))
        self.wait()

        btip = BTip().move_to(circles1[1].get_start())
        alpha = ValueTracker(0)
        target_mobj = circles1[1]
        def btip_updater(m):
            m.move_to(target_mobj.pfp(alpha.get_value()))
            m.tips.restore()
            direction = tangent_direction(target_mobj, alpha.get_value())
            m.tips.rotate(np.arctan2(direction[1], direction[0]))
            m.tips.move_to(m.circle)
        btip.tips.save_state()
        btip.tips.rotate(PI)
        self.play(ShowCreation(btip))
        btip.add_updater(btip_updater)
        self.play(alpha.animate.set_value(0.1))
        self.play(alpha.animate.set_value(0.4), run_time = 2)
        self.play(alpha.animate.set_value(0.95), run_time = 2.5)
        self.play(FadeOut(btip))

        bLeft = Rectangle(color = RED, fill_opacity = 0.7, stroke_width = 0)
        bLeft.surround(r_curve, buff = 0).stretch(0.4, 1).stretch(0.5, 0, about_point = bLeft.get_left())
        bRight = bLeft.copy().set_color(BLUE).next_to(bLeft, buff = 0)
        b = VGroup(bLeft, bRight)
        txtN = Text("N", color = RED).scale(2).next_to(b, LEFT)
        txtS = Text("S", color = BLUE).scale(2).next_to(b)
        self.play(ShowCreation(b))
        self.wait(0.5)
        self.play(FadeIn(txtN, RIGHT), FadeIn(txtS, LEFT))
        self.wait(2.5)
        self.play(
            *map(lambda m: FadeOut(m, run_time = 1), (
                b, txtN, txtS, 
                circles1, circles2, lineCenter,
                arrowTips1, arrowTips2, arrowTipsCenter
                )),
            FadeIn(battery), linePo.animate.set_stroke(opacity = (1, 1)), lineNe.animate.set_stroke(opacity = (1, 1)),
            frame.animate.set_euler_angles(theta = -30 * DEGREES, phi = 65 * DEGREES).set_width(frame_saved_width),
            run_time = 2)
        frame_theta_rate = -1
        frame.add_updater(frame_updater)
        self.wait(0.5)

        txtI = VGroup(Text("电流"), Tex("I")).set_color(RED).arrange().scale(0.8)
        txtN = VGroup(Text("绕圈匝数"), Tex("n")).set_color(GOLD).arrange().scale(0.8)
        txtIns = Text("插入铁芯", t2c = { "铁芯": GREY_B }).scale(0.8)
        vgUL = VGroup(txtI, txtN, txtIns).arrange(DOWN, aligned_edge = LEFT).to_corner(UL).fix_in_frame()
        #
        txt10 = Text("若增大通过的电流", t2c = { "电流": RED }).insert_n_curves(2).scale(0.8).to_edge(DOWN).fix_in_frame()
        txt11 = Text("或增加绕圈匝数", t2c = { "绕圈匝数": GOLD }).insert_n_curves(2).scale(0.8).to_edge(DOWN).fix_in_frame()
        txt12 = Text("都可以增强磁场", t2c = { "增强": GOLD, "磁场": PURPLE }).scale(0.8).to_edge(DOWN).fix_in_frame()
        txt13 = Text("在其中插入铁芯也可大大增强磁场", t2c = { "铁芯": GREY_B }).insert_n_curves(2).scale(0.8).to_edge(DOWN).fix_in_frame()
        #
        arrowI, arrowN = [IncreaseArrow(m) for m in [txtI[1], txtN[1]]]
        arrowI.set_color(RED)
        arrowN.set_color(GOLD)
        r_curve2 = RCurve(height = 6, w = 16.5, step_size = DEGREES, color = GOLD)\
            .apply_depth_test().rotate(90 * DEGREES, axis = UP).rotate(-90 * DEGREES, axis = LEFT).shift(OUT)
        cylinder = Cylinder(axis = RIGHT).move_to(rotate_center).scale(0.8).stretch(4.5, 0)
        disk1 = Circle(radius = 0.8).insert_n_curves(4).set_stroke(opacity = 0).set_fill(GREY, 1)\
            .apply_depth_test().rotate(89 * DEGREES, axis = UP).next_to(cylinder, LEFT, 0)
        disk2 = Circle(radius = 0.8).insert_n_curves(4).set_stroke(opacity = 0).set_fill(GREY, 1)\
            .apply_depth_test().rotate(-89 * DEGREES, axis = UP).next_to(cylinder, RIGHT, 0)
        #
        self.play(Write(txt10))
        self.play(AnimationGroup(FadeIn(txtI, RIGHT), Write(arrowI), lag_ratio = 0.5))
        self.wait(0.5)
        self.play(FadeIn(txt11, UP), FadeOut(txt10, UP * 0.5))
        self.play(AnimationGroup(FadeIn(txtN, RIGHT), Write(arrowN), lag_ratio = 0.5), Transform(r_curve, r_curve2))
        self.wait(0.8)
        self.play(FadeOut(txt11, run_time = 0.3), Write(txt12))
        self.wait()
        self.play(FadeOut(txt12, run_time = 0.3), Write(txt13))
        self.play(Write(txtIns), *map(lambda m: FadeIn(m, LEFT), (cylinder, disk1, disk2)))
        self.wait()
        self.play(FadeOut(txt13))
        self.wait(3)

class PhyElecB_CurveSubTextScene(Scene):
    def construct(self):
        txt1 = Text("且在其四周形成所示磁场", t2c = { "其四周": BLUE, "磁场": PURPLE }).scale(0.8).to_edge(DOWN, buff = LARGE_BUFF)
        txt2 = Text("我们此时引入一个小磁针", t2c = { "小磁针": BLUE }).scale(0.8)
        txt3 = Text("磁针N极指向与磁场方向一致", t2c = { "磁针N极": RED_B, "方向一致": GOLD }).scale(0.6)
        Group(txt2, txt3).arrange(DOWN).to_edge(DOWN, buff = LARGE_BUFF)
        txt4 = Text("此时的通电螺线(管)相当于一个条形磁铁", t2c = { "通电螺线(管)": BLUE, "条形磁铁": BLUE }).scale(0.8)
        txt5 = Text("左端为N极，右端为S极", t2c = { "N极": RED, "S极": BLUE }).scale(0.6)
        Group(txt4, txt5).arrange(DOWN).to_edge(DOWN, buff = LARGE_BUFF)
        self.play(Write(txt1))
        self.wait(2)
        self.play(FadeOut(txt1, run_time = 0.3), Write(txt2))
        self.wait(2)
        self.play(txt2.animate.next_to(txt3, UP), FadeIn(txt3, UP))
        self.wait(2)
        self.play(
            *map(lambda m: FadeOut(m, run_time = 0.3), (txt2, txt3)),
            Write(txt4)
            )
        self.wait(0.5)
        self.play(FadeIn(txt5, UP))
        self.wait(1.5)
        self.play(*map(FadeOut, (txt4, txt5)))
        
class PhyElecB_LineChapterScene(ChapterScene):
    CONFIG = {
        "str1": "Part 2",
        "str2": "通电直导线"
    }

class PhyElecB_LineScene(Scene):
    CONFIG = {
        "use_plot_depth": True
    }

    def construct(self):
        frame: CameraFrame = self.camera.frame
        frame.focal_distance = 50
        frame.set_euler_angles(theta = -90 * DEGREES, phi = -40 * DEGREES)

        self.add(txtwatermark())

        txt1 = Text("对于这根导线", t2c = { "导线": BLUE }).scale(0.8).to_edge(DOWN, 1.2)\
            .set_stroke(BLACK, width = 5, background = True).fix_in_frame()
        txt2 = Text("当我们通上电流时", t2c = { "电流": RED }, plot_depth = 100).scale(0.8).to_edge(DOWN, 1.2)\
            .set_stroke(BLACK, width = 5, background = True).fix_in_frame()
        txt3 = Text("会在垂直平面形成所示磁场", t2c = { "磁场": PURPLE }, plot_depth = 100).scale(0.7).to_edge(DOWN, 1.2)\
            .set_stroke(BLACK, width = 5, background = True).fix_in_frame()
        txt4 = Text("右手螺旋定则同样适用于该磁场环绕方向的判断", t2c = { "右手螺旋定则": BLUE, "环绕方向": BLUE })\
            .set_stroke(BLACK, width = 5, background = True).scale(0.8).to_edge(DOWN, 1.2).fix_in_frame()
        txt5 = Text("伸出拇指使其与电流同向", t2c = { "拇指": BLUE, "电流": BLUE, "同向": GOLD })\
            .set_stroke(BLACK, width = 5, background = True).scale(0.8).to_edge(DOWN, 1.2).fix_in_frame()
        txt6 = Text("收起其余四指，则该直导线周围磁场环绕直导线的方向，与该四指同向", t2c = { "其余四指": BLUE, "磁场环绕直导线的方向": PURPLE, "同向": GOLD })\
            .set_stroke(BLACK, width = 5, background = True).scale(0.7).to_edge(DOWN, 1.2).fix_in_frame()
        txt7 = Text("并且，增大电流可以增强磁场", t2c = { "电流": RED, "增强": GOLD, "磁场": PURPLE })\
            .set_stroke(BLACK, width = 5, background = True).scale(0.8).to_edge(DOWN, 1.2).fix_in_frame()

        line = Line(LEFT * 4.5, RIGHT * 4.5).apply_depth_test().shift(DOWN * 0.05)
        tip = ArrowTip().set_color(RED).move_to(line.get_right() + LEFT * 0.4)
        texI = Tex("I", color = RED).next_to(tip, DOWN).rotate(-PI / 2)
        self.play(GrowArrow(line), Write(txt1))
        self.wait(0.6)
        self.play(FadeOut(txt1, run_time = 0.3), FadeIn(txt2, UP), line.animate.set_color(RED), *map(FadeIn, (tip, texI)))
        self.play(Write(txt3), txt2.animate.next_to(txt3, UP))
        self.wait(0.5)

        rotate_center = LEFT * 0.2 + DOWN * 0.05
        def get_circle(buff = 1, path_arc = 70 * DEGREES):
            radius = buff
            rotate_points = (UP * radius, LEFT * radius, DOWN * radius, RIGHT * radius)
            rotate_arrows = VGroup()
            for i in range(len(rotate_points)):
                arrow = Arrow(rotate_points[i - 1], rotate_points[i], path_arc = path_arc)
                rotate_arrows.add(arrow)
            rotate_arrows.move_to(rotate_center).insert_n_curves(2 * buff).apply_depth_test()\
                .rotate(45 * DEGREES).rotate(89 * DEGREES, axis = UP).set_color(PURPLE)
            return rotate_arrows
        rotate_arrows_group = VGroup()
        for i in range(5):
            rotate_arrows_group.add(get_circle(2**i, (70 + 25 * i / 5) * DEGREES))
        rotate_arrows_group[-1].set_stroke(opacity = 0.8)
        try:
            rotate_arrows_group.save_state()
            self.play(Write(rotate_arrows_group))
        except:
            rotate_arrows_group.restore()
            self.add(rotate_arrows_group)
        self.play(
            frame.animate.set_euler_angles(phi = -10 * DEGREES, gamma = 30 * DEGREES),
            rotate_arrows_group.animate.rotate(-30 * DEGREES, axis = RIGHT),
            run_time = 3)
        self.play(
            frame.animate.set_euler_angles(phi = -25 * DEGREES, gamma = 0),
            rotate_arrows_group.animate.rotate(10 * DEGREES, axis = RIGHT),
            run_time = 3)
        texIL = Tex("I", color = RED).set_stroke(BLACK, 5, background = True).fix_in_frame().next_to(txt7[:5])
        self.wait(0.5)
        self.play(*map(lambda m: FadeOut(m, run_time = 0.3), (txt2, txt3)), Write(txt4))
        self.wait(0.8)
        self.play(FadeOut(txt4, run_time = 0.3), FadeIn(txt5))
        self.play(Write(txt6[:6]), txt5.animate.next_to(txt6, UP))
        self.wait(2)
        self.play(Write(txt6[6:]))
        self.wait()
        self.play(*map(FadeOut, (txt5, txt6)))
        self.play(Write(txt7[:5]))
        self.play(ShowCreation(texIL), run_time = 0.8)
        self.play(ReplacementTransform(texIL, txt7[5:7]))
        self.play(Write(txt7[7:]))
        self.wait(3)

class PhyElecB_RelChapterScene(ChapterScene):
    CONFIG = {
        "str1": "Part 3",
        "str2": "二者关系"
    }

class PhyElecB_RelScene(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(theta = 30 * DEGREES, phi = 70 * DEGREES)
        def frame_updater(frame: CameraFrame, dt):
            frame.increment_theta(DEGREES * dt)
        frame.add_updater(frame_updater)

        self.add(txtwatermark().fix_in_frame())

        txt1 = Text("对于这个通电的环形导线来说", t2c = { "环形导线": BLUE }).scale(0.8).to_edge(DOWN).fix_in_frame()
        circle = Circle(radius = 1.5, color = GOLD, n_components = 32).rotate(90 * DEGREES, axis = UP).apply_depth_test()
        circle.reverse_points()
        circle.set_points(circle.get_points()[:len(circle.get_points()) - 3])
        tip1 = ArrowTip(angle = 90 * DEGREES).set_color(RED).move_to(circle.get_edge_center(DOWN)).rotate(89 * DEGREES, axis = RIGHT)
        tip2 = ArrowTip(angle = 90 * DEGREES).set_color(RED).move_to(circle.get_edge_center(OUT))
        tip3 = ArrowTip(angle = -90 * DEGREES).set_color(RED).move_to(circle.get_edge_center(UP)).set_opacity(0.5).rotate(89 * DEGREES, axis = RIGHT)
        tips = VGroup(tip1, tip2, tip3)
        self.play(ShowCreation(circle))
        self.play(Write(tips))
        
