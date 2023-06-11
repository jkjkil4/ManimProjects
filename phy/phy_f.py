from manimlib import *

class Scene1(Scene):
    def construct(self) -> None:
        txt = Text("力的分解 - 定弦定角")
        
        self.play(DrawBorderThenFill(txt))
        self.wait()
        self.play(txt.animate.scale(0.6).to_edge(UP))

        line1 = Line(ORIGIN, LEFT + UP / np.sqrt(3))
        line2 = Line(ORIGIN, RIGHT + UP / np.sqrt(3))
        lines = VGroup(line1, line2).scale(2)
        circle = Circle()

        def circle_updater(_):
            div = line1.get_vector() + line2.get_vector()
            div /= get_norm(div)
            angle = angle_between_vectors(line1.get_vector(), line2.get_vector())
            d = circle.get_radius() / np.sin(angle / 2)
            circle.move_to(line1.get_start() + div * d)

        Group(lines, circle).move_to(ORIGIN)
        lines.shift(DOWN * 1.5).rotate(30 * DEGREES, about_point=line1.get_start())
        circle_updater(None)
        
        self.wait(0.5)
        self.play(AnimationGroup(FadeIn(lines), FadeIn(circle, scale=1.4), lag_ratio=0.2))

        circle.add_updater(circle_updater)

        self.play(Rotating(lines, -60 * DEGREES, about_point=line1.get_start(), rate_func=smooth), run_time = 1.5)
        self.play(Rotating(lines, 60 * DEGREES, about_point=line1.get_start(), rate_func=smooth), run_time = 1.5)

        g = Arrow(ORIGIN, DOWN * 3).set_color(BLUE)
        g2 = Arrow(ORIGIN, UP * 3).set_color(BLUE_E)
        def g_updater(m):
            m.shift(circle.get_center() - m.get_start())
        g.add_updater(g_updater)
        g2.add_updater(g_updater)
        
        self.wait(0.5)
        self.play(FadeIn(g))
        self.play(Rotating(lines, -20 * DEGREES, about_point=line1.get_start(), rate_func=smooth), run_time=1.2)
        self.play(FadeIn(g2))

        f1, f2 = Arrow(), Arrow()
        fs = Group(f1, f2).set_color(YELLOW)

        f2_shifted = False
        def fs_updater(_):
            angle = angle_between_vectors(line1.get_vector(), line2.get_vector())
            angle1 = abs(PI / 2 - angle_between_vectors(line1.get_vector(), g2.get_vector()))
            angle2 = abs(PI / 2 - angle_between_vectors(line2.get_vector(), g2.get_vector()))
            lth1 = g2.get_length() / np.sin(angle) * np.sin(angle2)
            lth2 = g2.get_length() / np.sin(angle) * np.sin(angle1) 
            f1.set_points_by_ends(circle.get_center(), circle.get_center() + rotate_vector(line1.get_unit_vector(), -PI / 2) * lth1)
            f2_start = f1.get_end() if f2_shifted else circle.get_center()
            f2.set_points_by_ends(f2_start, f2_start + rotate_vector(line2.get_unit_vector(), PI / 2) * lth2)
        fs.add_updater(fs_updater)

        f1_, f2_ = DashedLine(), DashedLine()
        fs_ = Group(f1_, f2_)

        def fs__updater(_):
            f1_.become(DashedLine(f2.get_end(), g2.get_end(), dash_length=0.1))
            f2_.become(DashedLine(f1.get_end(), g2.get_end(), dash_length=0.1))
            fs_.set_color(YELLOW)
        fs_.add_updater(fs__updater)

        rf1, rf2 = DashedLine(), DashedLine()
        rfs = Group(rf1, rf2).set_color(YELLOW)

        def rfs_updater(_):
            rf1.become(DashedLine(circle.get_center(), circle.get_center() - f1.get_unit_vector() * circle.get_radius(), dash_length=0.1))
            rf2.become(DashedLine(circle.get_center(), circle.get_center() - f2.get_unit_vector() * circle.get_radius(), dash_length=0.1))
            rfs.set_color(GREY)
        rfs.add_updater(rfs_updater)

        self.wait(0.5)
        self.play(FadeIn(rfs), FadeIn(fs))
        self.wait(1.5)
        self.play(FadeIn(fs_))

        self.wait()
        self.play(Rotating(lines, 20 * DEGREES, about_point=line1.get_start(), rate_func=smooth), run_time=1)
        self.play(Rotating(lines, -60 * DEGREES, about_point=line1.get_start()), run_time=6)

        circle2 = Circle(color=PURPLE)
        def circle2_updater(_):
            angle = angle_between_vectors(line1.get_vector(), line2.get_vector())
            angle2 = 2 * angle - PI / 2
            half = g2.get_length() / 2
            center = g2.get_center() + RIGHT * (half * np.tan(angle2))
            radius = half / abs(np.cos(angle2))
            circle2.become(Circle(radius=radius, color=PURPLE).move_to(center))

        self.wait()
        self.play(Rotating(lines, 14 * DEGREES, about_point=line1.get_start(), rate_func=smooth), run_time=1.5)
        self.wait(0.5)
        circle2_updater(None)
        self.bring_to_back(circle2)
        fs_.clear_updaters()
        fs.clear_updaters()
        self.play(f2.animate.move_to(f2_), FadeOut(fs_), FadeIn(circle2, scale=1.4), run_time = 2)
        f2_shifted = True
        fs.add_updater(fs_updater)
        circle2.add_updater(circle2_updater)

        self.play(Animation(fs), Rotating(lines, -14 * DEGREES, about_point=line1.get_start(), rate_func=smooth), run_time=1)
        self.play(Rotating(lines, 60 * DEGREES, about_point=line1.get_start()), run_time=6)
        self.play(Rotating(lines, -60 * DEGREES, about_point=line1.get_start()), run_time=6)
        self.wait(2)

class Scene2(Scene):
    def construct(self) -> None:
        circle = Circle(radius = 0.1)
        g = Arrow(ORIGIN, DOWN * 3, buff = 0).set_color(BLUE)
        g2 = Arrow(ORIGIN, UP * 3, buff = 0).set_color(BLUE_E)

        f1, f2 = Arrow(ORIGIN, LEFT + UP / np.sqrt(3)), Arrow(ORIGIN, RIGHT + UP / np.sqrt(3))
        line1, line2 = Line(ORIGIN, 20 * (LEFT + UP / np.sqrt(3))), Line(ORIGIN, 20 * (RIGHT + UP / np.sqrt(3)))
        ang = Arc(f2.get_angle(), 120 * DEGREES).scale(0.4, about_point=ORIGIN)
        fs = Group(line1, line2, f1, f2, ang)
        f1.set_color(YELLOW)
        f2.set_color(YELLOW)
        line1.set_color(GREY_D)
        line2.set_color(GREY_D)
        ang.set_color(RED)

        label = Tex('120^{\circ}', color=RED).scale(0.6)
        label.add_updater(lambda m: m.next_to(ang, UP, 0.05))

        f1_, f2_ = DashedLine(), DashedLine()
        fs_ = Group(f1_, f2_)

        f2_shifted = False
        def fs_updater(_):
            angle = angle_between_vectors(f1.get_vector(), f2.get_vector())
            angle1 = angle_between_vectors(f1.get_vector(), g2.get_vector())
            angle2 = angle_between_vectors(f2.get_vector(), g2.get_vector())
            lth1 = max(1e-2, g2.get_length() / np.sin(angle) * np.sin(angle2))
            lth2 = max(1e-2, g2.get_length() / np.sin(angle) * np.sin(angle1))
            f1.set_points_by_ends(ORIGIN, f1.get_unit_vector() * lth1)
            f2_center = f1.get_end() if f2_shifted else ORIGIN
            f2.set_points_by_ends(f2_center, f2_center + f2.get_unit_vector() * lth2)
        fs.add_updater(fs_updater)

        def fs__updater(_):
            f1_.become(DashedLine(f2.get_end(), g2.get_end(), dash_length=0.1))
            f2_.become(DashedLine(f1.get_end(), g2.get_end(), dash_length=0.1))
            fs_.set_color(YELLOW)
        fs_.add_updater(fs__updater)

        label1 = Tex('F_1', color=YELLOW).scale(0.6)
        label1.add_updater(lambda m: m.move_to(f1.get_start() + f1.get_unit_vector() * 0.4).shift(DL * 0.2))
        label2 = Tex('F_2', color=YELLOW).scale(0.6)
        label2.add_updater(
            lambda m: m.move_to(
                g2.get_end() - f2.get_unit_vector() * 0.4
                if f2_shifted
                else (f2.get_start() + f2.get_unit_vector() * 0.4)
            ).shift(DR * 0.2)
        )

        self.wait(0.5)
        self.play(*map(FadeIn, (label, label1, label2)), FadeIn(circle), FadeIn(g), FadeIn(fs))
        self.wait(0.5)
        self.play(FadeIn(g2))

        self.play(FadeIn(fs_))

        self.wait()
        self.play(Rotating(fs, 50 * DEGREES, about_point=f1.get_start(), rate_func=smooth), run_time=2)
        self.wait(0.5)
        self.play(Rotating(fs, -100 * DEGREES, about_point=f1.get_start()), run_time=6)

        circle2 = Circle(color=PURPLE)
        def circle2_updater(_):
            angle = angle_between_vectors(f1.get_vector(), f2.get_vector())
            angle2 = 2 * angle - PI / 2
            half = g2.get_length() / 2
            center = g2.get_center() + RIGHT * (half * np.tan(angle2))
            radius = half / abs(np.cos(angle2))
            circle2.become(Circle(radius=radius, color=PURPLE).move_to(center))

        self.wait()
        circle2_updater(None)
        self.bring_to_back(circle2)
        fs_.clear_updaters()
        fs.clear_updaters()
        fs.remove(ang)
        self.play(f2.animate.move_to(f2_), FadeOut(fs_), FadeIn(circle2, scale=1.4), FadeOut(ang), FadeOut(label), run_time = 2)
        f2_shifted = True
        fs.add_updater(fs_updater)
        circle2.add_updater(circle2_updater)

        self.play(Rotating(fs, -10 * DEGREES, about_point=f1.get_start(), rate_func=smooth), run_time=1.5)
        self.play(Rotating(fs, 120 * DEGREES, about_point=f1.get_start()), run_time=6)
        self.wait(0.5)
        self.play(Rotating(fs, -120 * DEGREES, about_point=f1.get_start()), run_time=6)
        self.wait(2)  

        