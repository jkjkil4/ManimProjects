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
    [1, -0.4, 0],
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

class Show(Scene):
    def construct(self):
        self.add(h.txtwatermark())
        h.chapter_animate(self, "Ⅰ", "效果展示", GREY_A)

class Use(Scene):
    def construct(self):
        self.add(h.txtwatermark())
        h.chapter_animate(self, "Ⅱ", "使用方法", GREY_A)

class Limit_1(Scene):
    def construct(self):
        self.add(h.txtwatermark())
        h.chapter_animate(self, "Ⅲ", "区域限制", GREY_A)

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

        
        
        