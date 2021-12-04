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

class PhyElecB_PictureScene1(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(theta = 12 * DEGREES, phi = 70 * DEGREES)

        r_curve = RCurve(height = 6, w = 10.5, step_size = DEGREES * 2, color = GOLD).reverse_points()\
            .apply_depth_test().rotate(90 * DEGREES, axis = UP).rotate(-90 * DEGREES, axis = LEFT)
        rect = Rectangle(FRAME_WIDTH - 5.6, FRAME_HEIGHT - 3.2, stroke_width = 6).fix_in_frame()
        arrow = Arrow(RIGHT * 4, LEFT * 4).set_color(PURPLE).apply_depth_test()

        self.add(r_curve, rect, arrow)

class PhyElecB_PictureScene2(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(theta = 112 * DEGREES, phi = 40 * DEGREES, gamma = 20 * DEGREES)

        iarrow = Arrow(IN * 6, OUT * 3).set_color(RED).apply_depth_test()
        rotate_arrows = VGroup()
        radius = 1.5
        rotate_points = [UP * radius, LEFT * radius, DOWN * radius, RIGHT * radius]
        for i in range(len(rotate_points)):
            arrow = Arrow(rotate_points[i - 1], rotate_points[i], path_arc = 70 * DEGREES)\
                .set_color(PURPLE).apply_depth_test()
            rotate_arrows.add(arrow)
        rect = Rectangle(FRAME_WIDTH - 8, FRAME_HEIGHT - 3.2, stroke_width = 6).fix_in_frame()

        self.add(iarrow, rotate_arrows, rect)

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
        self.play(*map(FadeOut, (b, txtN, txtS)))
        self.wait()

        def get_btip(mobj, alpha):
            btip = BTip().move_to(mobj.pfp(alpha) + OUT * 0.03)
            direction = tangent_direction(mobj, alpha)
            btip.tips.rotate(np.arctan2(direction[1], direction[0])).shift(OUT * 0.01)
            return btip
        btips = VGroup(
            get_btip(circles1[1], 0.02), get_btip(circles1[1], 0.3),
            get_btip(circles1[1], 0.55),
            get_btip(circles1[1], 0.75), get_btip(circles1[1], 0.96)
            )
        self.wait()
        for btip in btips:
            self.play(FadeIn(btip, scale = 0.8), run_time = 0.8)
        self.wait()
        self.play(FadeOut(btips))

        self.play(
            *map(lambda m: FadeOut(m, run_time = 1), (
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
        txt2 = Text("此时的通电螺线(管)相当于一个条形磁铁", t2c = { "通电螺线(管)": BLUE, "条形磁铁": BLUE }).scale(0.8)
        txt3 = Text("左端为N极，右端为S极", t2c = { "N极": RED, "S极": BLUE }).scale(0.6)
        Group(txt2, txt3).arrange(DOWN).to_edge(DOWN, buff = LARGE_BUFF)
        txt4 = Text("我们若引入小磁针", t2c = { "小磁针": BLUE }).scale(0.8)
        txt5 = Text("小磁针N极的指向与磁场方向一致", t2c = { "小磁针N极": RED_B, "方向一致": GOLD }).scale(0.6)
        Group(txt4, txt5).arrange(DOWN).to_edge(DOWN, buff = LARGE_BUFF)
        
        self.play(Write(txt1))
        self.wait(2)
        self.play(FadeOut(txt1, run_time = 0.3), Write(txt2))
        self.wait(0.5)
        self.play(FadeIn(txt3, UP))
        self.wait(1.5)
        self.play(
            *map(lambda m: FadeOut(m, run_time = 0.3), (txt2, txt3)),
            Write(txt4)
            )
        self.wait(2)
        self.play(txt4.animate.next_to(txt5, UP), FadeIn(txt5, UP))
        self.wait(2)
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

class PhyElecB_RelScene1(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(theta = 30 * DEGREES, phi = 70 * DEGREES)
        frame_anim_rate = 1
        def frame_updater(frame: CameraFrame, dt):
            frame.increment_theta(frame_anim_rate * DEGREES * dt)
        frame.add_updater(frame_updater)

        self.add(txtwatermark().fix_in_frame())

        txt1 = Text("对于这个通电的环形导线", t2c = { "环形导线": BLUE }).scale(0.8).to_edge(DOWN).fix_in_frame()
        circle = Circle(radius = 1.5, color = GOLD, n_components = 32).rotate(90 * DEGREES, axis = UP).apply_depth_test()
        circle.reverse_points()
        circle.set_points(circle.get_points()[:len(circle.get_points()) - 3])
        tip1 = ArrowTip(angle = 90 * DEGREES).set_color(RED).move_to(circle.get_edge_center(DOWN)).rotate(89 * DEGREES, axis = RIGHT)
        tip2 = ArrowTip(angle = 90 * DEGREES).set_color(RED).move_to(circle.get_edge_center(OUT))
        tip3 = ArrowTip(angle = -90 * DEGREES).set_color(RED).move_to(circle.get_edge_center(UP)).set_opacity(0.5).rotate(89 * DEGREES, axis = RIGHT)
        tips = VGroup(tip1, tip2, tip3)
        self.play(ShowCreation(circle))
        self.play(Write(tips), Write(txt1))
        self.wait()

        txt2 = Text("为了得出其四周磁场的分布情况", t2c = { "磁场": PURPLE, "分布情况": BLUE }).scale(0.8).fix_in_frame()
        txt3 = Text("可以将其等效为许多段直导线细分而成", t2c = { "直导线": BLUE, "细分": GOLD }).scale(0.8).fix_in_frame()
        Group(txt2, txt3).arrange(DOWN).to_edge(DOWN)
        def get_div_circle(n, **kwargs):
            vmobj = VMobject(**kwargs)
            vmobj.set_points_as_corners([circle.pfp(i / n) for i in range(n + 1)])
            return vmobj
        div_circle = get_div_circle(3, color = GOLD_E)
        self.play(FadeOut(txt1, run_time = 0.3), AnimationGroup(*map(Write, (txt2, txt3)), lag_ratio = 0.6))
        self.wait()
        self.play(FadeIn(div_circle))
        rt1, rt2 = 1.2, 0.1
        for i in range(4, 15):
            k = slow_into((i - 4) / 14)
            rt = rt1 * (1 - k) + rt2 * k
            self.play(div_circle.animate.become(get_div_circle(i, color = GOLD_E)), run_time = rt)
        self.wait(0.5)
        
        txt4 = Text("对其中的每一小段使用右手螺旋定则", t2c = { "每一小段": BLUE, "右手螺旋定则": BLUE }).scale(0.8).to_edge(DOWN).fix_in_frame()
        def get_db_dir_line(alpha, zoffset = RIGHT * 0.8):
            pos = circle.pfp(alpha)
            direction = np.arctan2(pos[2], pos[1])
            offset = UP * np.cos(direction) + OUT * np.sin(direction)
            offset *= 0.3
            return VGroup(
                Arrow(pos - offset + zoffset, pos - offset - zoffset, buff = 0), 
                Arrow(pos + offset - zoffset, pos + offset + zoffset, buff = 0)
                ).apply_depth_test().set_color(PURPLE)
        db_dir_lines = VGroup(*[get_db_dir_line(i / 4) for i in range(1, 4)])
        for mobj in db_dir_lines[0]:
            mobj.rotate(88.5 * DEGREES, axis = RIGHT)
        for mobj in db_dir_lines[2]:
            mobj.rotate(88.5 * DEGREES, axis = RIGHT)
        self.play(*map(lambda m: FadeOut(m, run_time = 0.3), (txt2, txt3, div_circle)), Write(txt4))
        for db_dir_line in db_dir_lines:
            self.wait(0.8)
            self.play(*map(GrowArrow, db_dir_line))
        frame_anim_rate = -1
        

        txt5 = Text("则从总体上来看，其中的磁场方向如图所示", t2c = { "总体": BLUE, "磁场方向": PURPLE }).scale(0.8).to_edge(DOWN).fix_in_frame()
        arrowCenter = Arrow(RIGHT * 4, LEFT * 4, tip_width_ratio = 8).set_color(PURPLE).apply_depth_test()
        self.play(FadeOut(txt4, run_time = 0.3), Write(txt5))
        self.play(AnimationGroup(db_dir_lines.animate.set_opacity(0.5)), GrowArrow(arrowCenter), lag_ratio = 0.4)
        self.wait(0.8)

        txt5_1 = Text("这实际上就是前面提到的通电螺线管的磁场判定方法", t2c = { "通电螺线管": BLUE, "判定方法": BLUE }).scale(0.8).to_edge(DOWN).fix_in_frame()
        rect = Rectangle(FRAME_WIDTH, FRAME_HEIGHT, color = YELLOW, stroke_width = 6).scale(0.6).fix_in_frame()
        self.play(FadeOut(txt5, run_time = 0.3), Write(txt5_1))
        self.play(FadeIn(rect), run_time = 0.8)
        self.wait(0.8)
        self.play(*map(FadeOut, (rect, txt5_1)), run_time = 0.8)

        frame.remove_updater(frame_updater)
        self.play(
            *map(FadeOut, (arrowCenter, db_dir_lines)),
            frame.animate.set_euler_angles(theta = 25 * DEGREES, phi = 35 * DEGREES), 
            run_time = 2)
        self.wait(0.5)

        # rotate_center = ORIGIN
        # c = Circle(color = PURPLE, stroke_width = 6).rotate(-PI / 2)\
        #     .reverse_points().next_to(rotate_center, UP, 0).stretch(0.8, 1, about_point = rotate_center).shift(UP * 0.8)
        # circles1 = VGroup(c)
        # for i in range(1, 3):
        #     k = i / 3
        #     pos = rotate_center + UP * 0.8 * (1 - k)
        #     c = c.copy().stretch(2.8, 0).stretch(3, 1).next_to(pos, UP, 0)
        #     circles1.add(c)
        # circles1.apply_depth_test().insert_n_curves(2)
        # circles2 = circles1.copy().stretch(-1, 1, about_point = rotate_center)
        # lineCenter = Line(RIGHT * 14, LEFT * 14, color = PURPLE, stroke_width = 6).apply_depth_test()
        # txt6 = Text("且形成所示磁场", t2c = { "磁场": PURPLE }).scale(0.8).to_edge(DOWN).set_stroke(BLACK, width = 4, background = True).fix_in_frame()
        # tip = ArrowTip(angle = PI, tip_width_ratio = 8).set_color(PURPLE).shift(LEFT * 3).apply_depth_test()
        # self.play(*map(lambda m: ShowCreation(m, run_time = 1.6), (circles1, circles2, lineCenter)), FadeIn(txt6))
        # self.play(FadeIn(tip), run_time = 0.5)
        # self.play(frame.animate.set_euler_angles(theta = 30 * DEGREES, phi = 42 * DEGREES), run_time = 2)
        # self.wait(0.5)
        # self.play(*map(FadeOut, (txt6, tip, circles1, circles2, lineCenter)))

        txt7 = Text("若将多个环形导线连接在一起", t2c = { "环形导线": BLUE, "连接在一起": GOLD })\
            .scale(0.8).to_edge(DOWN).fix_in_frame()
        txt8 = Text("就组成了一个螺线管", t2c = { "螺线管": BLUE }).scale(0.7).to_edge(DOWN).fix_in_frame()
        r_curve = RCurve(height = 6, w = 10.5, step_size = DEGREES, color = GOLD)\
            .apply_depth_test().rotate(90 * DEGREES, axis = UP).rotate(-90 * DEGREES, axis = LEFT)
        r_curve.reverse_points()
        passing = VMobject(color = RED)
        passing.set_points(r_curve.get_points())
        self.play(Write(txt7))
        self.play(
            Write(txt8), txt7.animate.next_to(txt8, UP),
            AnimationGroup(frame.animate.set_euler_angles(theta = 30 * DEGREES, phi = 65 * DEGREES), run_time = 2)
            )
        frame_anim_rate = 1
        frame.add_updater(frame_updater)
        self.play(*map(lambda m: FadeOut(m, run_time = 0.3), (tips, circle)), ShowCreation(r_curve))
        self.play(ShowPassingFlash(passing), run_time = 1.6)
        self.play(GrowArrow(arrowCenter.stretch(1.2, 0)))
        self.wait(2.5)

class PhyElecB_RelScene2(Scene):
    def construct(self):
        self.add(txtwatermark())

        txt1 = Text("也就是说通过右手螺旋定则", t2c = { "右手螺旋定则": BLUE }).scale(0.8).to_edge(DOWN)
        txt2 = Text("既可以建立左侧所示的关系，也可以建立右侧所示的关系", t2c = { "左侧": BLUE, "右侧": BLUE }).scale(0.7).to_edge(DOWN)
        rect1 = Rectangle(FRAME_WIDTH, FRAME_HEIGHT, stroke_width = 6, color = YELLOW).scale(0.35)
        rect2 = Rectangle(FRAME_WIDTH, FRAME_HEIGHT, stroke_width = 6, color = YELLOW).scale(0.35)
        Group(rect1, rect2).arrange(buff = LARGE_BUFF).move_to((txt1.get_center() + TOP) / 2)
        self.play(FadeIn(txt1))
        self.wait(0.5)
        self.play(txt1.animate.next_to(txt2, UP), Write(txt2[:12]))
        self.play(ShowCreation(rect1))
        self.wait()
        self.play(Write(txt2[12:]))
        self.play(ShowCreation(rect2))
        self.wait(2.5)

class PhyElecB_RelScene2_SubScene1(Scene):
    CONFIG = {
        "line_txt": "B",
        "curve_txt": "I",
        "line_color": PURPLE,
        "curve_color": RED
    }
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(phi = 30 * DEGREES, gamma = 20 * DEGREES).set_width(frame.get_width() * 0.6)

        self.line_tex = Tex(self.line_txt, color = self.line_color)
        self.curve_tex = Tex(self.curve_txt, color = self.curve_color)
        self.line = Arrow(IN * 8, OUT * 3.6).set_color(self.line_color).apply_depth_test()
        self.line.rotate(-90 * DEGREES)
        radius = 1.4
        rotate_points = (UP * radius, LEFT * radius, DOWN * radius, RIGHT * radius)
        self.curve = VGroup()
        for i in range(len(rotate_points)):
            arrow = Arrow(rotate_points[i - 1], rotate_points[i], path_arc = 70 * DEGREES).set_color(self.curve_color)
            self.curve.add(arrow)
        self.curve.rotate(40 * DEGREES).apply_depth_test()

        self.line_tex.next_to(self.line, RIGHT, aligned_edge = OUT).shift(DOWN * 0.2).rotate(90 * DEGREES, axis = RIGHT)
        self.curve_tex.next_to(self.curve, RIGHT)

        self.add(self.line_tex, self.curve_tex, self.line, self.curve)
        self.wait()

class PhyElecB_RelScene2_SubScene2(PhyElecB_RelScene2_SubScene1):
    CONFIG = {
        "line_txt": "I",
        "curve_txt": "B",
        "line_color": RED,
        "curve_color": PURPLE
    }

        