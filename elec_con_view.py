# ���´���δ����

import sys
sys.path.append(".")
import header as h
from manimlib import *

elecLineBuf = 2

class ElecConView(Scene):
    def construct():
        # ˮƽ�������
        lineElecConLeft = Line(UL, DL)
        lineElecConRight = Line(UR, DR)
        
        # ���ӵĵ�·
        lineLeft, lineRight = Line(), Line()
        def getLineCenter(line):    # ���ڵõ��߶��е�
            return (line.get_start() + line.get_end()) / 2
        # ʵʱ�趨��·���ߵ�λ��
        f_always(lineLeft.set_points_by_ends, lambda: getLineCenter(lineElecConLeft), lambda: getLineCenter(lineElecConLeft) - elecLineBuf)
        f_always(lineLeft.set_points_by_ends, lambda: getLineCenter(lineElecConRight), lambda: getLineCenter(lineElecConRight) + elecLineBuf)
        
        # ��·ĩ�˵�Բ
        lineLeftCircle, lineRightCircoe = Circle(), Circle()
        # ʵʱ�趨��·ĩ�˵�Բ��λ��
        always(lineLeftCircle.next_to, LEFT, buff = 0)
        always(lineRightCircle.next_to, RIGHT, buff = 0)