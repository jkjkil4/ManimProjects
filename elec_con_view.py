import sys
sys.path.append(".")
import header as h
from manimlib import *

elecLineBuf = [2, 0, 0]

class ElecConView(Scene):
    def construct(self):
        # 平行板电容器
        lineElecConLeft, lineElecConRight = Line(UL, DL).shift(DOWN / 2), Line(UR, DR).shift(DOWN / 2)
        groupLineElecCon = VGroup(lineElecConLeft, lineElecConRight)
        self.add(lineElecConLeft, lineElecConRight)
        
        # 连接的电路
        lineLeft, lineRight = Line(), Line()
        # 实时确定电路线段位置
        f_always(lineLeft.set_points_by_ends, lambda: h.getLineCenter(lineElecConLeft), lambda: h.getLineCenter(lineElecConLeft) - elecLineBuf)
        f_always(lineRight.set_points_by_ends, lambda: h.getLineCenter(lineElecConRight), lambda: h.getLineCenter(lineElecConRight) + elecLineBuf)
        self.add(lineLeft, lineRight)

        # 电路末端的圆
        lineLeftCircle, lineRightCircle = Circle(radius = 0.05, color = WHITE), Circle(radius = 0.05, color = WHITE)
        # 实时确定圆的位置
        always(lineLeftCircle.next_to, lineLeft, LEFT, buff = 0)
        always(lineRightCircle.next_to, lineRight, RIGHT, buff = 0)
        self.add(lineLeftCircle, lineRightCircle)

        self.play(*[FadeIn(mobject) for mobject in self.mobjects])
        self.wait(0.5)

        # 对电容器的描述
        txtCon = Text("这是一个平行板电容器").next_to(groupLineElecCon, DOWN, MED_LARGE_BUFF)
        self.play(Write(txtCon))
        self.wait()

        # 对接线的描述
        txtElec = VGroup(
            Text("其左端接电源"), Text("负极", color = BLUE), 
            Text(" 右端接电源"), Text("正极", color = RED)
            ).arrange().next_to(groupLineElecCon, DOWN, buff = MED_LARGE_BUFF)
        # 圆旁边的正负符号
        lineLeftSign, lineRightSign = Text("-", color = BLUE), Text("+", color = RED)
        # 实时确定符号的位置
        always(lineLeftSign.next_to, lineLeftCircle, LEFT, buff = SMALL_BUFF)
        always(lineRightSign.next_to, lineRightCircle, RIGHT, buff = SMALL_BUFF)
        self.play(FadeTransform(txtCon, txtElec), FadeIn(lineLeftSign), FadeIn(lineRightSign), run_time = 1.5)

        # 电压的描述
        txtU = VGroup(Text("电压为"), Tex("U", color = YELLOW).scale(1.5)).arrange().next_to(txtElec, DOWN)
        self.play(Write(txtU))
        self.wait()
        
        # 对两极板电性的描述
        txtConElec = VGroup(
            Text("则左板带"), Text("负电", color = BLUE),
            Text(" 右板带"), Text("正电", color = RED)
            ).arrange().next_to(groupLineElecCon, DOWN, buff = MED_LARGE_BUFF)
        # 符号标注
        sideSigns = []
        def signAlways(sign, line, k, offset):
            f_always(sign.move_to, lambda: h.getLineLerp(line, k) + [offset, 0, 0])
        for i in range(0, 4):
            signLeft, signRight = Text("-", color = BLUE), Text("+", color = RED)
            # 实时确定位置
            k = (i + 0.1) / 3.2
            signAlways(signLeft, lineElecConLeft, k, -MED_SMALL_BUFF)
            signAlways(signRight, lineElecConRight, k, MED_SMALL_BUFF)
            # 添加到sideSigns中
            sideSigns.append(signLeft)
            sideSigns.append(signRight)
        self.play(
            FadeOut(VGroup(txtElec, txtU), UP / 2), FadeIn(txtConElec, UP / 2), 
            *[FadeIn(sign) for sign in sideSigns]
            )
        self.wait()
        
        # 对电场强度的描述
        txtEp = VGroup(
            Text("电场强度", color = GOLD), Tex("E", color = GOLD).scale(1.5), Text("由"), 
            Text("正极板", color = RED), Text("指向"), Text("负极板", color = BLUE)
            ).arrange().next_to(groupLineElecCon, DOWN, buff = MED_LARGE_BUFF)
        # 电场强度
        eps = []
        for i in range(0, 6):
            ep = Arrow(fill_color = GOLD, max_width_to_length_ratio = 0.01)
            k = (i + 0.1) / 5.2
            ep.set_points_by_ends(h.getLineLerp(lineElecConRight, k) - [SMALL_BUFF, 0, 0], h.getLineLerp(lineElecConLeft, k) + [SMALL_BUFF, 0, 0])
            # 添加到eps中
            eps.append(ep)
        self.play(
            FadeOut(txtConElec, UP / 2), FadeIn(txtEp, UP / 2),
            *[GrowArrow(ep) for ep in eps]
            )
        def epAlways(ep, k):
            f_always(
                ep.set_points_by_ends, 
                lambda: h.getLineLerp(lineElecConRight, k) - [SMALL_BUFF, 0, 0], 
                lambda: h.getLineLerp(lineElecConLeft, k) + [SMALL_BUFF, 0, 0]
                )
        for i in range(0, 6):
            # 实时确定位置
            k = (i + 0.1) / 5.2
            epAlways(eps[i], k)
        self.wait()

        
        
        
        
        
        
        
        
        