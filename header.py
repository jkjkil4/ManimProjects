from manimlib import *

defaultFontSize = 36

def try_set(l, key, val):
    if key not in l:
        l[key] = val

def watermark():
    return ImageMobject("assets/self.webp", height = 4, opacity = 0.01)

def txtwatermark():
    return Text("jkjkil-jiang", font = "Noto Sans Black").scale(3.5).set_opacity(0.025) 

def getLineLerp(line, k):
    return line.get_start() * (1 - k) + line.get_end() * k

def running_end(t, pull_factor = -0.5):
    return 1 - running_start(1 - t, pull_factor)

def chapter_animate(self, str1, str2, color = GREY_E):
    txt1 = Text(str1, color = BLUE).set_stroke(BLUE_E, 3, background = True)
    txt2 = Text(str2, color = color)
    Group(txt1, txt2).arrange(buff = MED_LARGE_BUFF)
    self.play(DrawBorderThenFill(txt1), DrawBorderThenFill(txt2))
    self.wait()
    self.play(FadeOut(txt1), FadeOut(txt2))
    self.remove(txt1, txt2)

def dictAppend(a, b):
    a.update(b)
    return a

class RangeArrowTex(VGroup):
    CONFIG = {
        "line_config" : {},
        "tex_config" : {},
    }

    def __init__(self, mobj: Mobject, strtex: str, length: int, direction, **kwargs):
        super().__init__(**kwargs)

        if not "stroke_width" in self.line_config:
            self.line_config["stroke_width"] = 3
        if not "buff" in self.line_config:
            self.line_config["buff"] = 0.1
        
        rot = np.arctan2(direction[1], direction[0])
        xlen = length * np.cos(rot - PI / 2)
        ylen = length * np.sin(rot - PI / 2)
        v_offset = [xlen / 2, ylen / 2, 0]
        pos = mobj.get_edge_center(direction)
        self.line1 = Line(pos + v_offset, pos + v_offset + direction, **self.line_config)
        self.line2 = Line(pos - v_offset, pos - v_offset + direction, **self.line_config)
        self.tex = Tex(strtex, buff = 0.1, **self.tex_config).scale(0.8)
        self.arrow1 = Line(self.tex.get_left(), [-length / 2, 0, 0], **self.line_config).add_tip()
        self.arrow2 = Line(self.tex.get_right(), [length / 2, 0, 0], **self.line_config).add_tip()

        self.tex.move_to(pos + direction).shift(-direction / np.sqrt(direction[0]**2 + direction[1]**2) / 2)
        self.arrow1.rotate(rot - PI / 2, about_point = ORIGIN).shift(self.tex.get_center())
        self.arrow2.rotate(rot - PI / 2, about_point = ORIGIN).shift(self.tex.get_center())

        self.add(self.line1, self.line2, self.arrow1, self.arrow2, self.tex)

class Explain(VGroup):
    def __init__(self, pos, direction, mtxt, dotcolor = BLUE_E, linecolor = BLUE, **kwargs):
        if isinstance(mtxt, str):
            mtxt = self.mtxt(mtxt)
        pos_ = sum([np.array(one) for one in pos]) / len(pos) if isinstance(pos, list) else pos
        lines = \
            [Line(one, pos_ + direction, color = linecolor, buff = 0.02) for one in pos] \
            if isinstance(pos, list) \
            else [Line(pos_, pos_ + direction, color = linecolor, buff = 0.02)]
        points = \
            [Circle(radius = 0.03, color = dotcolor).set_fill(dotcolor, opacity = 1).move_to(one) for one in pos] \
            if isinstance(pos, list) \
            else [Circle(radius = 0.03, color = dotcolor).set_fill(dotcolor, opacity = 1).move_to(pos)]
        mtxt.next_to(pos_ + direction, direction, SMALL_BUFF)
        super().__init__(*lines, *points, mtxt, **kwargs)
    
    @staticmethod
    def mtxt(txt, txtcolor = BLUE_B):
        return Text(txt, color = txtcolor).scale(0.8)

class ThreeDBorder(SGroup):
    def __init__(self, obj: Surface, buff = 0, **kwargs):
        if not "gloss" in kwargs:
            kwargs["gloss"] = 0
        if not "shadow" in kwargs:
            kwargs["shadow"] = 0
        super().__init__(**kwargs)
        def add_borders(flist, direction):
            self.add(
                *[Line3D(
                    obj.get_edge_center(a + direction) + (a + direction) * buff, 
                    obj.get_edge_center(a - direction) + (a - direction) * buff,
                    **kwargs) 
                for a in flist]
                )
        add_borders([UL, UR, DL, DR], OUT)
        add_borders([LEFT + OUT, LEFT + IN, RIGHT + OUT, RIGHT + IN], UP)
        add_borders([UP + OUT, UP + IN, DOWN + OUT, DOWN + IN], LEFT)

class SucAbleFadeIn(MoveToTarget):
    def __init__(self, mobj, direction = ORIGIN):
        mobj.generate_target()
        mobj.shift(-direction).set_opacity(0)
        super().__init__(mobj)

class HeaderTestScene(Scene):
    def construct(self):
        line = Line()
        arrow = RangeArrowTex(line, "U", 2, UP)
        self.add(line, arrow)
        self.wait()

        # tracker = ValueTracker(PI / 2)
        p = Point()
        for i in range(0, 361, 2):
            val = i / 360 * TAU + PI / 2
            self.remove(arrow)
            arrow = RangeArrowTex(
                line, "U", 2, 
                (np.cos(val) * RIGHT + np.sin(val) * UP) * 2
                )
            self.add(arrow)
            self.wait(0.01)
        # self.play(tracker.animate.set_value(TAU), run_time = 3)

class OpeningScene(Scene): # 6s
    str1 = ""
    str2 = ""
    style = 0
    img_time = 1
    txt1_time = 1
    txt2_time = 1

    def construct(self):
        self.wait(0.4)

        imgSelf = ImageMobject("assets/self.png", height = 1)
        tmp = imgSelf.copy()
        txt = Text(self.str1, color = WHITE if self.style else BLACK)
        group = Group(tmp, txt).arrange()
        self.play(FadeIn(imgSelf), imgSelf.animate.shift(getPos(tmp)), run_time = self.img_time)
        self.wait(0.4)
        self.play(Write(txt), run_time = self.txt1_time)
        self.wait(0.6)
        txt2 = Text(self.str2, color = "#aaaaaa" if self.style else "#555555").next_to(group, DOWN)
        self.play(Write(txt2), run_time = self.txt2_time)
        self.wait()
        self.play(*[FadeOut(mobject) for mobject in self.mobjects], run_time = 1)
class InfoScene(Scene): # 6s
    info_list = []
    column_count = 2
    wait_time = 4
    def get_background(self):
        return Rectangle(
            2 * (FRAME_X_RADIUS - DEFAULT_MOBJECT_TO_EDGE_BUFFER), 
            2 * (FRAME_Y_RADIUS - DEFAULT_MOBJECT_TO_EDGE_BUFFER),
            ).set_stroke(BLUE_E, 2).set_fill(BLUE_E, 0.1)
    def get_mobj(self, info):
        return Text(info, color = WHITE).scale(0.8)
        
    def construct(self):
        background = self.get_background()

        info_mobjs = []
        x = background.get_left()[0]
        y = background.get_top()[1]
        xoffset = (background.get_width() - 2 * DEFAULT_MOBJECT_TO_EDGE_BUFFER) / self.column_count
        index = 0
        for info in self.info_list:
            mobj = self.get_mobj(info)
            if len(info_mobjs) == 0:
                mobj.align_to([x, y], UL).shift(DEFAULT_MOBJECT_TO_EDGE_BUFFER * DR)
            else:
                mobj.next_to(info_mobjs[index - 1], DOWN, aligned_edge = LEFT)
                if(mobj.get_bottom()[1] - DEFAULT_MOBJECT_TO_EDGE_BUFFER < background.get_bottom()[1]):
                    x += xoffset
                    mobj.align_to([x, y], UL).shift(DEFAULT_MOBJECT_TO_EDGE_BUFFER * DR)
            info_mobjs.append(mobj)
            index += 1

        self.play(FadeIn(background), *[Write(mobj) for mobj in info_mobjs], run_time = 1)
        self.wait(self.wait_time)
        self.play(FadeOut(background), *[Uncreate(mobj) for mobj in info_mobjs], run_time = 1)
class TimeScene(InfoScene):
    def get_mobj(self, info):
        return VGroup(Text(info[0], color = BLUE).insert_n_curves(50), Text(info[1]).insert_n_curves(50))\
            .arrange().set_stroke(BLUE_E, 4, background = True, opacity = 0.6).scale(0.9)
class ChapterScene(Scene):
    CONFIG = {
        "str1": "Part ?",
        "str2": "测试"
    }
    def construct(self):
        txt1 = Text(self.str1, color = BLUE).scale(1.6).insert_n_curves(2)
        txt1_ = txt1.copy().scale(2).set_opacity(0.2)
        txt2 = Text(self.str2).scale(1.2).insert_n_curves(2)
        txt2_ = txt2.copy().scale(1.6).set_opacity(0.2)
        Group(txt1, txt2).arrange(DOWN)
        Group(txt1_, txt2_).arrange(DOWN, buff = MED_LARGE_BUFF)
        txt1.shift(LEFT * 0.2)
        txt2.shift(RIGHT * 0.2)
        txt1_.shift(LEFT * 0.4)
        txt2_.shift(RIGHT * 0.4)
        self.play(
            FadeIn(txt1_, RIGHT * 4), FadeIn(txt2_, LEFT * 4),
            FadeIn(txt1, RIGHT * 2), FadeIn(txt2, LEFT * 2), 
            rate_func = lambda t: rush_from(rush_from(t)), run_time = 2)
        self.play(
            FadeOut(txt1_, RIGHT * 4), FadeOut(txt2_, LEFT * 4),
            FadeOut(txt1, RIGHT), FadeOut(txt2, LEFT),
            rate_func = lambda t: rush_into(rush_into(t)))
class EndScene(Scene):
    strAuthor = "jkjkil-jiang"
    strTool = "manim(动画) kdenlive(剪辑)"
    strBgm = "Unknown"
    def construct(self):
        txtAuthor = VGroup(
            Text("作者", color = BLUE),
            Text(self.strAuthor, color = GREY)
            ).scale(0.7).arrange().to_edge(UL, LARGE_BUFF)
        txtTool = VGroup(
            Text("工具", color = BLUE), 
            Text(self.strTool, color = GREY)
            ).scale(0.7).arrange().next_to(txtAuthor, DOWN, MED_LARGE_BUFF, LEFT)
        txtBgm = VGroup(
            Text("bgm", color = BLUE),
            Text(self.strBgm, color = GREY)
            ).scale(0.7).arrange().to_edge(DL, LARGE_BUFF)
        
        self.play(*[DrawBorderThenFill(mobj) for mobj in [txtAuthor, txtTool, txtBgm]])
        self.wait(2)

# class GMRoomPlane(VGroup):
#     def __init__(self, xlen, ylen, color, **kwargs):
#         self.np = NumberPlane((0, xlen), (0, ylen)).apply_matrix([[1, 0], [0, -1]]).set_color(color)
#         self.npOrig = Dot(self.np.c2p(), color = BLACK)
#         self.npXArrow = Arrow(self.np.x_axis.get_start(), self.np.x_axis.get_end() + RIGHT * 0.3, buff = 0).set_fill(BLACK)
#         self.npYArrow = Arrow(self.np.y_axis.get_start(), self.np.y_axis.get_end() + DOWN * 0.3, buff = 0).set_fill(BLACK)
#         self.npXLabel = Tex("x", color = BLACK).scale(1.5).next_to(self.npXArrow)
#         self.npYLabel = Tex("y", color = BLACK).scale(1.5).next_to(self.npYArrow, DOWN)
#         super().__init__(*[self.np, self.npOrig, self.npXArrow, self.npYArrow, self.npXLabel, self.npYLabel], **kwargs)

#     def animate1(self):
#         return ShowCreation(self.np, lag_ratio = 0.01)
#     def animate2Array(self):
#         return [FadeIn(self.npOrig, scale_factor = 1.3), 
#             GrowArrow(self.npXArrow), GrowArrow(self.npYArrow),
#             DrawBorderThenFill(self.npXLabel), DrawBorderThenFill(self.npYLabel)]

class CodeLines(VGroup):
    def __init__(self, texts, t2c):
        super().__init__()
        for text in texts:
            self.add(Text(text, color = GREY_E, t2c = t2c).scale(0.6))
        self.arrange(DOWN, aligned_edge = LEFT, buff = SMALL_BUFF)

    def replaceAnimate(self, fn, index, text, color = GREY_E, t2c = {}, animate = ReplacementTransform):
        new = Text(text, color = color, t2c = t2c).scale(0.6)
        old = self[index]
        new.move_to(old.get_left(), LEFT)
        fn(animate(old, new))
        self.replace_submobject(index, new)

    def removeAnimate(self, index, animate = FadeOut):
        sub = self[index]
        self.remove(sub)
        ul = self.get_corner(UL)
        return AnimationGroup(FadeOut(sub), self.animate.arrange(DOWN, aligned_edge = LEFT, buff = SMALL_BUFF).move_to(ul, UL))
class CodeBackground(BackgroundRectangle):
    CONFIG = {
        "fill_color": "#EBEBEB",
        "fill_opacity": 1,
        "stroke_width": 1,
        "stroke_opacity": 1,
        "stroke_color": GREY_E,
        "buff": 0.2
    }
class CodeHeader(Rectangle):
    CONFIG = {
        "fill_opacity": 1,
        "stroke_width": 1,
        "stroke_opacity": 1,
        "stroke_color": GREY_E,
    }
class CodeView(VGroup):
    def __init__(self, title, texts, t2c, titleColor = WHITE, headerColor = GREY_D):
        self.lines = CodeLines(texts, t2c)
        self.background = CodeBackground(self.lines)
        txtTitle = Text(title, color = titleColor).scale(0.5)
        self.header = CodeHeader(self.background.get_width(), txtTitle.get_height() + 0.2, fill_color = headerColor)
        self.header.move_to(self.background.get_top() + [0, self.header.get_height() / 2, 0])
        txtTitle.move_to(self.header)
        self.others = VGroup(self.header, self.background, txtTitle)
        super().__init__(self.others, self.lines)
