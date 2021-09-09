import sys
sys.path.append(".")
import header as h
from manimlib import *

poly_vertexs = [
    [-1, 1, 0],
    [-0.2, 1.3, 0],
    [0.3, 1, 0],
    [0, 0, 0],
    [1, 1.7, 0],
    [1, 0.2, 0],
    [1.4, -0.4, 0],
    [0.9, -0.4, 0],
    [-0.2, -1, 0],
    [-0.5, -0.8, 0]
]
for vertex in poly_vertexs:
    for i in range(0, len(vertex)):
        vertex[i] *= 1.6
def iloop(i):
    if(i < 0):
        return i + len(poly_vertexs)
    if(i >= len(poly_vertexs)):
        return i - len(poly_vertexs)
    return i
poly_lines = VGroup()
for i in range(0, len(poly_vertexs)):
    poly_lines.add(Line(poly_vertexs[i], poly_vertexs[iloop(i + 1)]))

class PBOpeningScene(h.OpeningScene):
    str1 = "多边形框——限制、遮罩与叠加"
    str2 = "算法分享"
    style = 1
    img_time = 1.3
    txt1_time = 1.5

class PBTimeScene(h.TimeScene):
    info_list = [
        ["00:13", "效果展示"]
    ]

class Show(Scene):
    def construct(self):
        self.add(h.txtwatermark())
        h.chapter_animate(self, "1", "效果展示", GREY_A)

class Use_1(Scene):
    def construct(self):
        self.add(h.txtwatermark())
        h.chapter_animate(self, "2", "使用方法", GREY_A)

        txt1 = Text("上述功能在 GameMaker Studio 2 中实现", t2c = { "GameMaker Studio 2": BLUE })
        txt2 = Text("需要2.3及以上版本", color = GREY).scale(0.8)
        g1_2 = Group(txt1, txt2).arrange(DOWN)
        self.play(DrawBorderThenFill(txt1))
        self.play(ShowCreation(txt2))
        self.wait()

        txt3 = Text("如果你需要将其用到其它GMS2项目中", t2c = { "其它GMS2项目": GOLD }).scale(0.8)
        txt4 = Text("你只需要转移以下内容中的代码即可", t2c = { "以下内容": GOLD }).scale(0.8)
        txtC1 = Text("oPolygonBorder", color = BLUE).scale(0.8)
        txtC2 = Text("Script", color = GREEN).scale(0.8)
        txtC3 = Text("shaderDrawStroke", color = ORANGE).scale(0.8)
        Group(txt3, txt4).arrange(DOWN)
        self.play(FadeOut(g1_2, UP), FadeIn(txt3, UP))
        self.wait()
        self.play(Write(txt4))
        self.play(txt4.animate.to_corner(UP), FadeOut(txt3))
        Group(txtC1, txtC2, txtC3).arrange(DOWN, buff = LARGE_BUFF * 1.5).next_to(txt4, DOWN, LARGE_BUFF)
        self.play(*[FadeIn(txt) for txt in [txtC1, txtC2, txtC3]])
        self.wait(1.5)
        
        def to_left(mobj):
            l = Text("-")
            l.move_to(mobj)
            l.to_corner(LEFT)
            self.play(FadeIn(l), mobj.animate.next_to(l, RIGHT), run_time = 0.6)
            return l
        tl1 = to_left(txtC1)
        tl2 = to_left(txtC2)
        tl3 = to_left(txtC3)
        def notice(mobj, under):
            l = Line(mobj.get_left(), mobj.get_right(), color = YELLOW).next_to(mobj, DOWN, SMALL_BUFF)
            under.next_to(l, DOWN, SMALL_BUFF)
            self.play(GrowArrow(l), FadeIn(under, UP))
            self.wait()
            self.play(Uncreate(l), FadeOut(under, DOWN))
        
        txtC1_ = Text("(Object) 多边形框的主要部分", t2c = { "Object": BLUE, "多边形框": GOLD, "主要": YELLOW })\
            .scale(0.8).next_to(txtC1, DOWN, aligned_edge = LEFT)
        txtC2_ = Text("其中包含 drawSurfaceStrokeColor viewX viewY viewW viewH", t2c = { "[5:27]": GREEN, "[28:]": GREY })\
            .insert_n_curves(50).scale(0.8).next_to(txtC2, DOWN, aligned_edge = LEFT)
        txtC3_ = Text("(Shader) 用于当使用遮罩或叠加框时，对多边形进行描边以达到绘制边框的效果", t2c = { "Shader": ORANGE, "使用遮罩": BLUE, "叠加框": BLUE, "绘制边框": BLUE })\
            .scale(0.8).next_to(txtC3, DOWN, aligned_edge = LEFT)
        self.play(Write(txtC1_))
        self.wait()
        self.play(Write(txtC2_), run_time = 3)
        notice(txtC2_[5:27], Text("用于方便调用shaderDrawStroke", t2c = { "shaderDrawStroke": ORANGE }).scale(0.6))
        notice(txtC2_[28:], Text("不重要").insert_n_curves(50).scale(0.6))
        self.play(Write(txtC3_), run_time = 3)
        self.wait(2)

        titleLine = Line().next_to([0, TOP[1] - DEFAULT_MOBJECT_TO_EDGE_BUFFER - txtC1_.get_height() / 0.8, 0], DOWN)
        self.play(*[FadeOut(mobj) for mobj in [txt4, txtC2, txtC3, txtC2_, txtC3_, tl1, tl2, tl3]])
        self.wait(0.5)
        self.play(FadeOut(txtC1_), txtC1.animate.scale(1 / 0.8).to_corner(UP).set_x(0), GrowArrow(titleLine))


class Limit_1(Scene):
    def construct(self):
        self.add(h.txtwatermark())
        h.chapter_animate(self, "3", "原理", GREY_A)
        h.chapter_animate(self, "3-1", "区域限制", GREY_A)

        txt1 = Text("区域限制可以分为两步")
        txt2 = VGroup(
            Text("检测点是否在多边形内", color = BLUE),
            Text("和"),
            Text("当不在多边形内时限制到多边形内", color = BLUE)
            ).arrange()
        VGroup(txt1, txt2).arrange(DOWN)
        self.play(DrawBorderThenFill(txt1))
        self.play(Write(VGroup(txt2[0])))
        self.wait(0.5)
        self.play(Write(VGroup(txt2[1], txt2[2])), run_time = 1.5)
        self.wait(0.8)
        self.play(Indicate(txt2[0][0:2]), Indicate(txt2[2][8:10]), run_time = 1.5)
        self.wait()
        
        title: Text = txt2[0]
        titleLine = Line().next_to([0, TOP[1] - DEFAULT_MOBJECT_TO_EDGE_BUFFER - title.get_height(), 0], DOWN)
        self.play(
            FadeOut(Group(txt1, txt2[1:3])), GrowArrow(titleLine), 
            title.animate.move_to(ORIGIN).to_edge(UP).set_color(WHITE)
            )
        self.wait(0.8)

        poly_offset = LEFT * 4 + DOWN * 0.5
        poly_lines.shift(poly_offset)
        poly_dot = Dot(radius = 0.07, color = YELLOW).move_to([-0.5, 0.7, 0] + poly_offset)
        self.play(Write(poly_lines), Write(poly_dot))
        self.wait(0.8)

        txtCheck1 = Text("为了检测点是否在多边形内", t2c = { "[2:12]": BLUE })\
            .next_to(titleLine, DOWN, LARGE_BUFF, LEFT).scale(0.8)
        txtCheck2 = Text("我们可以过点作一条水平线", t2c = { "作一条水平线": ORANGE })\
            .scale(0.8).next_to(txtCheck1, DOWN, aligned_edge = LEFT)
        self.play(Write(txtCheck1))
        self.wait(0.5)
        self.play(Write(txtCheck2))

        poly_horlines = VGroup()
        def update_poly_horline():
            size = len(poly_vertexs)
            x = poly_dot.get_x() - poly_offset[0]
            y = poly_dot.get_y() - poly_offset[1]
            
            # 从末尾开始遍历得到第一个不为水平的线的 走向 和 交点情况
            isAllHor = True
            prevTrend = False
            prevHasIntersection = False
            prev = poly_vertexs[size - 1]
            for i in range(size - 2, -1, -1):
                cur = poly_vertexs[i]
                if(prev[1] != cur[1]):
                    isAllHor = False
                    prevTrend = cur[1] < prev[1]	# 因为是反向遍历，所以是小于（和后面的大于相反）
                    prevHasIntersection = (y >= min(prev[1], cur[1]) and y <= max(prev[1], cur[1]))
                    break
                prev = cur
            if(isAllHor):	# 如果全部都为水平线，则返回False
                return False
            
            # 计算交点横坐标
            intersections = []
            prev = poly_vertexs[size - 1]
            for i in range(0, size):
                cur = poly_vertexs[i]
                hasIntersection = False
                if(prev[1] != cur[1]):
                    trend = cur[1] > prev[1]
                    if(trend != prevTrend or not prevHasIntersection):
                        if(y >= min(prev[1], cur[1]) and y <= max(prev[1], cur[1])):
                            hasIntersection = True
                            intersections.append(prev[0] + (cur[0] - prev[0]) * (y - prev[1]) / (cur[1] - prev[1]))
                    if(trend != prevTrend):
                        prevTrend = trend
                prevHasIntersection = hasIntersection
                prev = cur
            if(len(intersections) == 0):	# 如果没有交点，则返回False
                return False
            
            intersections.sort()
            self.remove(*poly_horlines)
            poly_horlines.remove(*poly_horlines)
            poly_horlines.set_submobjects([])
            poly_horlines.add(Line([intersections[0] - 0.5, y, 0] + poly_offset, [intersections[0], y, 0] + poly_offset, color = RED))
            isInside = True
            for i in range(0, len(intersections) - 1):
                poly_horlines.add(
                    Line(
                        [intersections[i], y, 0] + poly_offset, [intersections[i + 1], y, 0] + poly_offset,
                        color = GREEN if isInside else RED
                        ))
                isInside = not isInside
            last = len(intersections) - 1
            poly_horlines.add(Line([intersections[last], y, 0] + poly_offset, [intersections[last] + 0.5, y, 0] + poly_offset, color = RED))

            isInside = False
            for intersection in intersections:
                if(intersection > x):
                    return isInside
                isInside = not isInside
            return False
        def update_poly_horline_and_add():
            result = update_poly_horline()
            for horline in poly_horlines:
                self.add(horline)
            return result
        auto_update_poly_horline = False
        block_update_poly_horline = False
        # f_always(poly_dot.set_fill, )
        poly_dot.add_updater(
            lambda o: o.set_fill(GREEN if update_poly_horline_and_add() else RED) 
                if auto_update_poly_horline and not block_update_poly_horline else None
            )

        update_poly_horline()
        for horline in poly_horlines:
            horline.tmpcolor = horline.get_color()
            horline.set_color(WHITE)

        length_total = sum([horline.get_length() for horline in poly_horlines])
        for horline in poly_horlines:
            self.play(GrowArrow(horline), rate_func = linear, run_time = horline.get_length() / length_total * 0.5)
        
        txtCheck3 = Text("多边形将水平线分割为多个部分", t2c = { "多边形": GOLD, "水平线": GOLD, "[7:14]": ORANGE }).scale(0.8)
        txtCheck4 = Text("其中在和不在多边形内部的区域交替出现", t2c = { "在": GREEN, "不在": RED, "交替出现": BLUE }).scale(0.8)
        txtCheck5 = Text("我是用计算与各边交点的方法来实现的", t2c = { "[3:10]": ORANGE }).scale(0.8)
        Group(txtCheck3, txtCheck4, txtCheck5).arrange(DOWN, aligned_edge = LEFT).next_to(txtCheck2, DOWN, aligned_edge = LEFT)
        self.play(Write(txtCheck3))
        self.wait(0.5)
        self.play(Write(txtCheck4))
        self.play(*[horline.animate.set_color(horline.tmpcolor) for horline in poly_horlines])
        self.play(Indicate(txtCheck4[2:3]), ShowCreationThenFadeAround(poly_horlines[1]), ShowCreationThenFadeAround(poly_horlines[3]))
        self.play(
            Indicate(txtCheck4[4:6]), ShowCreationThenFadeAround(poly_horlines[2]),
            ShowCreationThenFadeAround(poly_horlines[0]), ShowCreationThenFadeAround(poly_horlines[4])
            )
        block_update_poly_horline = True
        self.play(poly_dot.animate.set_color(GREEN))
        block_update_poly_horline = False
        self.wait(0.5)
        self.play(Write(txtCheck5))
        self.wait()

        txtCheck6 = Text("当水平线穿过顶点时，有种特殊情况", t2c = { "穿过顶点": BLUE, "分为两种情况": ORANGE }).scale(0.8)
        txtCheck7 = Text("当水平线穿过如图所示的位置时", t2c = { "如图所示": GOLD }).scale(0.8).insert_n_curves(50)
        txtCheck8 = Text("按照计算与各边交点的方法，这里会得到两个交点", t2c = { "[2:9]": ORANGE }).scale(0.8)
        txtCheck9 = Text("（相邻两边各一个）", color = GREY).scale(0.6)
        txtCheck10 = Text("此时该顶点左右两边的判断是相同的", t2c = { "相同": GREEN }).scale(0.8)
        self.play(
            txtCheck5.animate.next_to(txtCheck1.get_left(), buff = 0),
            *[FadeOut(txt) for txt in [txtCheck1, txtCheck2, txtCheck3, txtCheck4]]
            )
        txtCheck6.next_to(txtCheck5, DOWN, aligned_edge = LEFT)
        Group(txtCheck7, txtCheck8, txtCheck9, txtCheck10).arrange(DOWN, aligned_edge = LEFT).next_to(txtCheck6, DOWN, MED_LARGE_BUFF, LEFT)
        self.play(Write(txtCheck6), run_time = 1.6)
        self.wait(0.5)
        auto_update_poly_horline = True
        self.play(Write(txtCheck7), poly_dot.animate.move_to([poly_dot.get_x(), poly_offset[1], 0]), run_time = 1.2)
        auto_update_poly_horline = False
        self.play(Flash(poly_offset, line_length = 0.15))
        self.wait(0.5)
        self.play(Write(txtCheck8))
        self.play(Write(txtCheck9))
        self.play(Write(txtCheck10), Flash(poly_offset, line_length = 0.15, color = GREEN))
        self.wait(1.5)
        self.play(*[FadeOut(txt) for txt in [txtCheck7, txtCheck8, txtCheck9, txtCheck10]])
        
        txtCheck11 = Text("按照计算与各边交点的方法，这里也会得到两个交点", t2c = { "[2:9]": ORANGE, "也": BLUE }).scale(0.8)
        txtCheck12 = Text("但此时该顶点两边的判断是相反的", t2c = { "相反": RED }).scale(0.8)
        txtCheck13 = Text("所以此时我将这两个交点仅当做一个交点来处理", t2c = { "此时": BLUE, "[11:18]": ORANGE }).scale(0.8)
        txtCheck14 = Text("以保证在判断时，两边的判断是相反的", t2c = { "相反": RED }).scale(0.8)
        Group(txtCheck11, txtCheck12, txtCheck13, txtCheck14).arrange(DOWN, aligned_edge = LEFT).next_to(txtCheck7, DOWN, aligned_edge = LEFT)
        auto_update_poly_horline = True
        self.play(Write(txtCheck7), poly_dot.animate.move_to([poly_dot.get_x(), 0.32 + poly_offset[1], 0]), run_time = 1.2)
        auto_update_poly_horline = False
        self.play(Flash(poly_vertexs[5] + poly_offset, line_length = 0.15))
        self.wait(0.5)
        self.play(Write(txtCheck11))
        self.wait(0.5)
        self.play(Write(txtCheck12), Flash(poly_vertexs[5] + poly_offset, line_length = 0.15, color = RED))
        self.wait()
        self.play(Write(txtCheck13))
        self.wait(0.5)
        self.play(Write(txtCheck14))
        self.wait(1.5)
        self.play(*[FadeOut(txt) for txt in [txtCheck5, txtCheck6, txtCheck7, txtCheck11, txtCheck12, txtCheck13, txtCheck14]])

        txtCheck15 = Text("当水平线与一条边重合时，也有特殊情况", t2c = { "[4:10]": BLUE }).scale(0.8).next_to(txtCheck5.get_left(), RIGHT, 0)
        txtCheck16 = Text("此时将这条边忽略", t2c = { "忽略": ORANGE }).scale(0.8)
        txtCheck17 = Text("将相邻两边认为是直接连接的即可", t2c = { "直接连接": BLUE }).scale(0.8)
        Group(txtCheck16, txtCheck17).arrange(DOWN, aligned_edge = LEFT).next_to(txtCheck15, DOWN, aligned_edge = LEFT)
        auto_update_poly_horline = True
        self.play(Write(txtCheck15), poly_dot.animate.move_to([poly_dot.get_x(), -0.4 * 1.6 + poly_offset[1], 0]), run_time = 1.2)
        auto_update_poly_horline = False
        self.play(ShowCreationThenFadeAround(poly_lines[6]))
        self.wait(0.8)
        self.play(Write(txtCheck16))
        self.play(Write(txtCheck17))
        self.wait(1.5)
        self.play(*[FadeOut(mobj) for mobj in [poly_lines, poly_dot, txtCheck15, txtCheck16, txtCheck17, poly_horlines]])

class Limit_2(Scene):
    def construct(self):
        self.add(h.txtwatermark())

        title = Text("检测点是否在多边形内").to_corner(UP)
        titleLine = Line().next_to(title, DOWN)
        self.add(title, titleLine)
        self.play(Transform(title, Text("将点限制到多边形内").to_corner(UP)))
        self.wait(0.8)

        poly_dot = Dot(radius = 0.07, color = YELLOW).shift(RIGHT * 2 + DOWN * 0.3)
        poly_lines.shift(DOWN * 0.5 + LEFT)
        self.play(Write(poly_lines), Write(poly_dot))

        arrow = Arrow(poly_dot.get_center(), poly_dot.get_center() + [-0.9, -0.6, 0], buff = 0).set_fill(BLUE)
        txt1 = Text("只需得到离多边形边框最近的位置即可", t2c = { "最近": BLUE })\
            .insert_n_curves(50).scale(0.8).next_to(poly_lines, DOWN, 0.75).set_x(0)
        txt2 = Text("（得到与每条边的最近位置，再看看哪个相距最短）", color = GREY).scale(0.6).next_to(txt1, DOWN)
        self.play(Write(txt1))
        self.play(GrowArrow(arrow))
        self.play(Write(txt2))
        self.wait(2)
        self.play(*[FadeOut(mobj) for mobj in [title, titleLine, poly_dot, poly_lines, arrow, txt1, txt2]])
        
class Mask(Scene):
    def construct(self):
        self.add(h.txtwatermark())
        h.chapter_animate(self, "3-2", "遮罩绘制", GREY_A)

        txt1 = Text("要想只在框内绘制（遮罩）", t2c = { "框内": BLUE }).shift(UP * 0.3)
        txt2 = Text("就需要将框内部的区域用合适的方式表达出来", t2c = { "内部的区域": BLUE, "表达": ORANGE }).next_to(txt1, DOWN)
        self.play(DrawBorderThenFill(txt1))
        self.wait(0.5)
        self.play(Write(txt2))
        self.wait()

        poly_offset = LEFT * 4 + DOWN * 0.5
        poly_lines.shift(poly_offset)
        self.play(FadeOut(txt1, UP), FadeOut(txt2, UP), Write(poly_lines), run_time = 2)

        txtT1 = Text("在这里，我用到了三角剖分算法", t2c = { "三角剖分": GOLD })\
            .scale(0.8).next_to(poly_lines, LARGE_BUFF, RIGHT).to_corner(UP, LARGE_BUFF)
        txtT2 = Text("也就是一种可以将多边形内部用许多三角形表示的算法", t2c = { "多边形内部": GOLD, "三角形": GOLD })\
            .scale(0.8).next_to(txtT1, DOWN, aligned_edge = LEFT)
        self.play(DrawBorderThenFill(txtT1))
        self.wait(0.6)
        self.play(Write(txtT2))

        def tri(a, b, c):
            result = Triangle(fill_opacity = 0.5).set_color(GOLD)
            a_, b_, c_ = poly_vertexs[a] + poly_offset, poly_vertexs[b] + poly_offset, poly_vertexs[c] + poly_offset
            result.set_points_as_corners([a_, b_, c_, a_])
            return result
        def iloop(i, ilen):
            if(i < 0):
                return i + ilen
            if(i >= ilen):
                return i - ilen
            return i
        clip_buff = [i for i in range(0, len(poly_vertexs))]
        clip_index_list = [6, 7, 8, 4, 5, 1, 2, 3]

        tmp_clip_buff = clip_buff.copy()
        cliped = VGroup().set_fill(GOLD)
        for index in clip_index_list:
            cliped_index = tmp_clip_buff.index(index)
            ilen = len(tmp_clip_buff)
            cliped.add(tri(index, tmp_clip_buff[iloop(cliped_index + 1, ilen)], tmp_clip_buff[iloop(cliped_index - 1, ilen)]))
            tmp_clip_buff.pop(cliped_index)
        self.play(Write(cliped), run_time = 1.5)
        self.wait(1.5)
        self.play(FadeOut(cliped))
        self.wait(0.5)

        txtT3 = Text("首先我们要找到一个凸顶点", t2c = { "凸顶点": GOLD }).scale(0.8).next_to(txtT2, DOWN, MED_LARGE_BUFF, LEFT)
        txtT4 = Text("如这里是一个凸顶点", t2c = { "是": GREEN, "凸顶点": GOLD }).scale(0.8).next_to(txtT3, DOWN, aligned_edge = LEFT)
        txtT5 = Text("这里则不是一个凸顶点", t2c = { "不是": RED, "凸顶点": GOLD }).scale(0.8).next_to(txtT3, DOWN, aligned_edge = LEFT)
        self.play(DrawBorderThenFill(txtT3))
        self.wait(0.5)
        self.play(Write(txtT4), run_time = 0.7)
        self.play(Flash(poly_vertexs[6] + poly_offset, color = GREEN))
        self.wait(0.8)
        self.play(Transform(txtT4, txtT5), run_time = 0.7)
        self.play(Flash(poly_offset, color = RED))
        self.wait()
        self.play(FadeOut(txtT4))

        tmp_clip_buff = clip_buff.copy()
        tmp_poly_lines = [*poly_lines]
        def clip_animate(i):
            index = clip_index_list[i]
            cliped_index = tmp_clip_buff.index(index)

            if len(tmp_poly_lines) <= 3:
                a, b = FadeIn(cliped[i]), AnimationGroup(*[FadeOut(line) for line in tmp_poly_lines], cliped[i].animate.set_opacity(0.1))
                tmp_clip_buff.clear()
                tmp_poly_lines.clear()
                return a, b

            remove_line1 = tmp_poly_lines[cliped_index]
            remove_line2 = tmp_poly_lines[iloop(cliped_index - 1, len(tmp_clip_buff))]
            tmp_poly_lines.remove(remove_line1)
            tmp_poly_lines.remove(remove_line2)
            tmp_clip_buff.pop(cliped_index)
            insert_index = iloop(cliped_index - 1, len(tmp_clip_buff))
            insert_line = Line(
                poly_vertexs[tmp_clip_buff[insert_index]] + poly_offset,
                poly_vertexs[tmp_clip_buff[iloop(cliped_index, len(tmp_clip_buff))]] + poly_offset
                )
            tmp_poly_lines.insert(insert_index, insert_line)

            return FadeIn(cliped[i]), AnimationGroup(FadeIn(insert_line), FadeOut(remove_line1), 
                FadeOut(remove_line2), cliped[i].animate.set_opacity(0.1))
        txtT6 = Text("比如对于这个凸顶点").scale(0.8)
        txtT7 = Text("将其从多边形的顶点中移除的同时", t2c = { "移除": ORANGE }).scale(0.8)
        txtT8 = Text("产生一个新的多边形和一个三角区域", t2c = { "新的多边形": BLUE, "三角区域": BLUE }).scale(0.8)
        txtT9 = Text("对于其他的凸顶点也可以作同样的操作", t2c = { "同样的操作": ORANGE }).scale(0.8)
        gT6_T9 = Group(txtT6, txtT7, txtT8, txtT9).arrange(DOWN, aligned_edge = LEFT).next_to(txtT3, DOWN, aligned_edge = LEFT)
        self.play(DrawBorderThenFill(txtT6))
        self.play(Flash(poly_vertexs[6] + poly_offset))
        self.wait(0.8)
        animate1, animate2 = clip_animate(0)
        self.play(Write(txtT7))
        self.play(animate1)
        self.wait(0.5)
        self.play(Write(txtT8))
        self.play(animate2)
        self.wait(0.8)
        self.play(DrawBorderThenFill(txtT9))
        self.wait()
        for i in range(1, 3):
            animate1, animate2 = clip_animate(i)
            self.play(animate1, run_time = 0.7)
            self.play(animate2, run_time = 0.7)
            self.wait(0.2)
        self.wait(0.5)
        self.play(FadeOut(gT6_T9), FadeOut(txtT3))

        txtT10 = Text("但是对于这个凸顶点").scale(0.8)
        txtT11 = Text("当移除它后，所产生的多边形出现了边相交的情况", t2c = { "移除": ORANGE, "边相交": RED }).scale(0.8)
        txtT12 = Text("因此这时是不能移除这个凸顶点的", t2c = { "不能": RED }).scale(0.8)
        line0_5 = Line(poly_vertexs[0] + poly_offset, poly_vertexs[5] + poly_offset, color = GOLD)
        gT10_T12 = Group(txtT10, txtT11, txtT12).arrange(DOWN, aligned_edge = LEFT).next_to(txtT2, DOWN, MED_LARGE_BUFF, LEFT)
        self.play(DrawBorderThenFill(txtT10))
        self.play(Flash(poly_vertexs[9] + poly_offset))
        self.wait(0.8)
        self.play(Write(txtT11))
        self.play(GrowArrow(line0_5), *[line.animate.set_color(RED) for line in poly_lines[2:4]])
        self.wait(0.8)
        self.play(Write(txtT12))
        self.wait(1.5)
        self.play(FadeOut(gT10_T12), Uncreate(line0_5), *[line.animate.set_color(WHITE) for line in poly_lines[2:4]])

        txtT13 = Text("继续对其他顶点进行判断和处理").scale(0.8)
        txtT14 = Text("当多边形变为凸多边形时", t2c = { "凸多边形": GOLD }).scale(0.8)
        txtT15 = Text("将一个顶点和其他顶点相连即可分割", t2c = { "分割": ORANGE }).scale(0.8)
        gT13_T15 = Group(txtT13, txtT14, txtT15).arrange(DOWN, aligned_edge = LEFT).next_to(txtT2, DOWN, MED_LARGE_BUFF, LEFT)
        line1 = Line(poly_vertexs[0] + poly_offset, poly_vertexs[2] + poly_offset, color = GOLD)
        line2 = Line(poly_vertexs[0] + poly_offset, poly_vertexs[3] + poly_offset, color = GOLD)
        self.play(DrawBorderThenFill(txtT13))
        for i in range(3, 5):
            animate1, animate2 = clip_animate(i)
            self.play(animate1, run_time = 0.7)
            self.play(animate2, run_time = 0.7)
            self.wait(0.2)
        self.wait()
        self.play(Write(txtT14))
        self.wait(0.5)
        self.play(Write(txtT15))
        self.play(GrowArrow(line1), GrowArrow(line2))
        for i in range(5, 8):
            animate1, animate2 = clip_animate(i)
            self.play(animate1, run_time = 0.4)
            self.play(animate2, run_time = 0.4)
            if(i == 5):
                self.remove(line1)
            if(i == 6):
                self.remove(line2)
        self.wait()
        self.play(*[clip.animate.set_opacity(0.5) for clip in cliped], run_time = 0.5)
        self.play(*[clip.animate.set_opacity(1).set_fill(GOLD, opacity = 0.5) for clip in cliped], run_time = 0.5)
        self.wait()

        txtLast1 = Text("这样我们就将多边形的内部").scale(0.8)
        txtLast2 = Text("表示了出来", t2c = { "表示": ORANGE }).scale(0.8)
        group = Group(txtLast1, txtLast2).arrange(DOWN, aligned_edge = LEFT).next_to(txtT15, DOWN, MED_LARGE_BUFF, LEFT)
        self.play(Write(txtLast1))
        self.play(Write(txtLast2))
        self.wait(1.5)
        self.play(FadeOut(cliped), *[FadeOut(mobj) for mobj in [txtT1, txtT2, gT13_T15, group]])


        