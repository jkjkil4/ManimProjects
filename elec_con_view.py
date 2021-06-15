# 以下代码未测试

import sys
sys.path.append(".")
import header as h
from manimlib import *

elecLineBuf = 2

class ElecConView(Scene):
    def construct():
        # 水平板电容器
        lineElecConLeft = Line(UL, DL)
        lineElecConRight = Line(UR, DR)
        
        # 连接的电路
        lineLeft, lineRight = Line(), Line()
        def getLineCenter(line):    # 用于得到线段中点
            return (line.get_start() + line.get_end()) / 2
        # 实时设定电路连线的位置
        f_always(lineLeft.set_points_by_ends, lambda: getLineCenter(lineElecConLeft), lambda: getLineCenter(lineElecConLeft) - elecLineBuf)
        f_always(lineLeft.set_points_by_ends, lambda: getLineCenter(lineElecConRight), lambda: getLineCenter(lineElecConRight) + elecLineBuf)
        
        # 电路末端的圆
        lineLeftCircle, lineRightCircoe = Circle(), Circle()
        # 实时设定电路末端的圆的位置
        always(lineLeftCircle.next_to, LEFT, buff = 0)
        always(lineRightCircle.next_to, RIGHT, buff = 0)