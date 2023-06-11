import sys
sys.path.append(".")
import header_legacy as h
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

class Limit_1(Scene):
    def construct(self):
        poly_offset = DOWN * 0.5
        poly_lines.shift(poly_offset)
        poly_dot = Dot(radius = 0.07, color = YELLOW).move_to([-0.5, 0.7, 0] + poly_offset)
        self.play(Write(poly_lines), Write(poly_dot))
        self.wait()

        self.poly_horlines = VGroup()
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

            poly_new_horlines = VGroup()
            poly_new_horlines.add(Line([intersections[0] - 0.5, y, 0] + poly_offset, [intersections[0], y, 0] + poly_offset, color = RED))
            isInside = True
            for i in range(0, len(intersections) - 1):
                poly_new_horlines.add(
                    Line(
                        [intersections[i], y, 0] + poly_offset, [intersections[i + 1], y, 0] + poly_offset,
                        color = GREEN if isInside else RED
                        ))
                isInside = not isInside
            last = len(intersections) - 1
            poly_new_horlines.add(Line([intersections[last], y, 0] + poly_offset, [intersections[last] + 0.5, y, 0] + poly_offset, color = RED))
            self.remove(self.poly_horlines)
            self.add(poly_new_horlines)
            self.poly_horlines = poly_new_horlines
            # print(self.poly_horlines.get_y(), poly_new_horlines.get_y())

            isInside = False
            for intersection in intersections:
                if(intersection > x):
                    return isInside
                isInside = not isInside
            return False

        update_poly_horline()
        self.remove(self.poly_horlines)
        for horline in self.poly_horlines:
            horline.tmpcolor = horline.get_color()
            horline.set_color(WHITE)

        def get_length(mobj):
            return mobj.get_right()[0] - mobj.get_left()[0]

        length_total = sum([get_length(horline) for horline in self.poly_horlines])
        for horline in self.poly_horlines:
            self.play(GrowArrow(horline), rate_func = linear, run_time = get_length(horline) / length_total * 0.5)
        self.wait()
        
        self.play(*[horline.animate.set_color(horline.tmpcolor) for horline in self.poly_horlines])
        self.play(poly_dot.animate.set_color(GREEN))
        self.wait()

        auto_update_poly_horline = True
        def dot_updater(o):
            if auto_update_poly_horline:
                o.set_fill(GREEN if update_poly_horline() else RED)
        poly_dot.add_updater(dot_updater)

        auto_update_poly_horline = True
        self.play(poly_dot.animate.move_to([poly_dot.get_x(), poly_offset[1], 0]), run_time = 1.2)
        auto_update_poly_horline = False
        self.play(Flash(poly_offset, line_length = 0.15))
        self.wait()
        
        auto_update_poly_horline = True
        self.play(poly_dot.animate.move_to([poly_dot.get_x(), 0.32 + poly_offset[1], 0]), run_time = 1.2)
        auto_update_poly_horline = False
        self.play(Flash(poly_vertexs[5] + poly_offset, line_length = 0.15))
        self.wait()

        auto_update_poly_horline = True
        self.play(poly_dot.animate.move_to([poly_dot.get_x(), -0.4 * 1.6 + poly_offset[1], 0]), run_time = 1.2)
        auto_update_poly_horline = False
        self.play(ShowCreationThenFadeAround(poly_lines[6]))
        self.wait(2)
