from numbers import Number
import sys
sys.path.append('.')
from manimlib import *
from header import *

class PhyEquip(VGroup):
    CONFIG = {
        "radius": 1
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        circle_points = Arc.create_quadratic_bezier_points(TAU, n_components = 64)
        vmobj = VMobject()
        vmobj.append_points(circle_points * 0.9)
        vmobj.append_points(circle_points)
        vmobj.scale(self.radius).set_stroke("#eeeeee", width = 1).set_fill(opacity = 1)

        self.add(vmobj)

class PhyEquipTxt(PhyEquip):
    def __init__(self, txt, txtscale = 1, **kwargs):
        super().__init__(**kwargs)

        self.txt = txt = Text(txt)
        distance = np.sqrt(txt.get_right()[0] ** 2 + txt.get_top()[1] ** 2)
        r = self.get_right()[0] * 0.65
        txt.scale(r / distance * txtscale)
        self.add(txt)

class PhyEquipVMobj(PhyEquip):
    def __init__(self, vmobj: VMobject, objscale = 1, **kwargs):
        super().__init__(**kwargs)

        maxdistance = max([np.sqrt(p[0] ** 2 + p[1] ** 2) for p in vmobj.get_all_points()])
        r = self.get_right()[0] * 0.95
        vmobj.scale(r / maxdistance * objscale)
        self.vmobj = vmobj
        self.add(vmobj)

class PhyEquipLight(PhyEquipVMobj):
    def __init__(self, **kwargs):
        rect = Rectangle(1, 0.06).set_stroke(width = 0).set_fill(opacity = 1)
        self.vg = VGroup(rect.copy().rotate(PI / 4), rect.copy().rotate(-PI / 4))
        super().__init__(self.vg, **kwargs)

class LinedPhyEquip(VGroup):
    def __init__(self, phyEquip: PhyEquip, lineLength = 2, lineSize = 0.1, buff = 0):
        self.phyEquip = phyEquip
        rect = Rectangle(lineLength, lineSize).set_fill(WHITE, opacity = 1).set_stroke(width = 0)
        self.lineLeft = rect.copy().next_to(phyEquip, LEFT, buff)
        self.lineRight = rect.copy().next_to(phyEquip, RIGHT, buff)

        super().__init__(self.lineLeft, self.lineRight, phyEquip)

class PhyArrowEquip(VGroup):
    class Txt(Text):
        def __init__(self, txt):
            super().__init__(txt, font = "Noto Sans Thin")
            self.scale(0.6)
    class NumTxt(Text):
        def __init__(self, txt):
            super().__init__(txt, font = "Noto Sans Thin")
            self.scale(0.3)
    
    CONFIG = {
        "txtclass" : Txt,
        "numtxtclass" : NumTxt,
        "line_width" : 1,
        "arrow_enabled": True,
        # arc
        "arc_radius" : 1,
        "arc_rad" : PI / 2,
        # grad
        "grad_fn" : linear,
        "grad_cnt" : 4,
        "grad_half_len" : 0.1,
        "grad_len_fn": lambda i: 1 if i % 10 == 0 else (0.75 if i % 5 == 0 else 0.5),
        "grad_up": True,
        "grad_down": True,
        "grad_up_range" : None,
        "grad_down_range" : None,
        "grad_up_step" : None,
        "grad_down_step" : None,
        "grad_zero_offset" : 0,
        "grad_num_buff" : 0.05
    }
    
    def __init__(self, txt: str = "", **kwargs):
        super().__init__(**kwargs)

        if self.grad_up_range == None:
            self.grad_up_range = (0, self.grad_cnt)
        if self.grad_down_range == None:
            self.grad_down_range = (0, self.grad_cnt)
        self.arc_start_angle = (PI + self.arc_rad) / 2
        self.grad_total_cnt = self.grad_cnt * 10

        # 中间文字
        self.txt = self.txtclass(txt).move_to([0, self.arc_radius / 2, 0])

        # 圆弧
        self.arc = Arc(self.arc_start_angle, -self.arc_rad, radius = self.arc_radius).set_stroke(width = self.line_width * 1.5)

        # 刻度
        self.grads = VGroup()
        for i in range(self.grad_total_cnt + 1):
            rot = self.grad_rot(i)
            x = np.cos(rot) * self.arc_radius
            y = np.sin(rot) * self.arc_radius
            ghl = self.grad_half_len * self.grad_len_fn(i)
            xoffset = np.cos(rot) * ghl
            yoffset = np.sin(rot) * ghl
            start = [x + xoffset, y + yoffset, 0] if self.grad_up else [x, y, 0]
            end = [x - xoffset, y - yoffset, 0] if self.grad_down else [x, y, 0]
            self.grads.add(Line(start, end).set_stroke(width = self.line_width))

        # 刻度数字
        self.up_nums, self.down_nums = VGroup(), VGroup()
        if self.grad_up_step != None:
            self.generate_nums(self.grad_up_range, self.grad_up_step, 1, self.grad_num_buff, self.up_nums)
        if self.grad_down_step != None:
            self.generate_nums(self.grad_down_range, self.grad_down_step, -1, self.grad_num_buff, self.down_nums)
        
        self.wo_arrow = VGroup(self.txt, self.arc, self.grads, self.up_nums, self.down_nums)

        self.add(self.wo_arrow)

        # 指针
        if self.arrow_enabled:
            self.arrow_offset = ValueTracker(0)
            self.point = Dot().set_opacity(0)
            self.arrow = Line().set_color(BLUE).set_stroke(width = self.line_width * 2)
            def arrow_updater(m: Line):
                k = (self.arrow_offset.get_value() + self.grad_zero_offset * 10)
                rot = self.grad_rot(k)
                fst = self.grads[0].get_center() - self.point.get_center()
                radius = np.sqrt(fst[0]**2 + fst[1]**2) + self.grad_half_len / 2
                m.set_points_by_ends(self.point.get_center(), self.point.get_center() + [radius * np.cos(rot), radius * np.sin(rot), 0])
            self.arrow.add_updater(arrow_updater)
        if self.arrow_enabled:
            self.add(self.point, self.arrow)
    
    def grad_rot(self, ind):
        return self.arc_start_angle - self.grad_fn(ind / self.grad_total_cnt) * self.arc_rad
    def numstr(self, val):
        result = '%.1f' % val
        if result.endswith('.0'):
            result = result[:len(result) - 2]
        return result

    def generate_nums(self, g_range, step, sign, buff, vg):
        for i in range(g_range[0], g_range[1] + 1):
            rot = self.grad_rot(i * 10)
            direction = RIGHT * np.cos(rot) + UP * np.sin(rot)
            txt = self.numstr(step * (i - self.grad_zero_offset))
            num = self.numtxtclass(txt)
            num.move_to(direction * (self.arc_radius + sign * (self.grad_half_len + num.get_height() / 2 + buff)))
            num.rotate(rot - PI / 2)
            vg.add(num)

class PhyMaterialEquip(PhyArrowEquip):
    def __init__(
        self, txt: str, wire_base_color: tuple = (), wire_base_txt: tuple = (),
        wire_base_radius = 0.06, bottom_rect_height = 0.4, srdrect_buff = SMALL_BUFF, **kwargs
        ):
        if len(wire_base_color) < len(wire_base_txt):
            raise Exception("len(wire_base_color) 必须大于或等于 len(wire_base_txt)")

        super().__init__(txt, **kwargs)

        # 外框
        self.surrounding_rect = SurroundingRectangle(self, buff = srdrect_buff).set_stroke(WHITE)
        self.bottom_rect = Rectangle(self.surrounding_rect.get_width(), bottom_rect_height)\
            .next_to(self.surrounding_rect, DOWN, 0).set_fill(GREY_B, opacity = 1)

        # 接线座
        self.wire_base = VGroup()
        steps = len(wire_base_color) + 1
        circle_points = Arc.create_quadratic_bezier_points(TAU, n_components = 32)
        wire_tmp = VMobject().append_points(circle_points * wire_base_radius).append_points(circle_points * wire_base_radius * 0.4)
        for i in range(0, len(wire_base_color)):
            color = wire_base_color[i]
            x = self.bottom_rect.get_left()[0] + self.bottom_rect.get_width() * (i + 1) / steps
            wire = wire_tmp.copy().set_stroke(color = color, width = 1).set_fill(color, opacity = 1).move_to([x, self.bottom_rect.get_y(), 0])
            self.wire_base.add(wire)
        self.wire_base_txt = VGroup()
        for i in range(0, len(wire_base_txt)):
            txt = Text(wire_base_txt[i], color = GREY_D, font = "Noto Sans Thin", t2c = { "|": GREY_B }).scale(0.3).next_to(self.wire_base[i], DOWN, 0.02)
            self.wire_base_txt.add(txt)

        self.add(self.surrounding_rect, self.bottom_rect, self.wire_base, self.wire_base_txt)

class PhyMultiEquip(VGroup):
    CONFIG = {
        "line_width" : 1,
        "box_buff": 0.1,
        "arrow_fn": linear
    }
    SWITCH_CNT = 18
    SWITCH_PER_ANGLE = TAU / SWITCH_CNT

    class NumTxt(Text):
        def __init__(self, txt):
            super().__init__(txt, font = "Noto Sans Thin")
            self.scale(0.12)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 刻度
        self.grad_omega_side, self.grad_omega_vg_txt, self.grad_omega = vg_grad_omega = self.initOmegaGrads()
        self.grad_DC_side, self.grad_DC_vg_txt, self.grad_DC = vg_grad_DC = self.initDCGrads()
        self.grad_AC_side, self.grad_AC_vg_txt, self.grad_AC = vg_grad_AC = self.initACGrads()
        vgGrads = VGroup(vg_grad_omega, vg_grad_DC, vg_grad_AC)

        # 指针
        self.arrow_offset = ValueTracker(0)
        self.point = Dot().set_opacity(0)
        self.arrow = Line().set_color(BLUE).set_stroke(width = self.line_width * 2)
        def arrow_updater(m: Line):
            k = self.arrow_offset.get_value()
            rot1 = 0.75 * PI
            rot2 = 0.25 * PI
            rot = (1 - k) * rot1 + k * rot2
            fst = self.grad_omega.grads[0].get_center() - self.point.get_center()
            radius = np.sqrt(fst[0]**2 + fst[1]**2) + self.grad_omega.grad_half_len / 2
            m.set_points_by_ends(self.point.get_center(), self.point.get_center() + [radius * np.cos(rot), radius * np.sin(rot), 0])
        self.arrow.add_updater(arrow_updater)

        # 刻度下方Tex
        self.tex = Tex("\\rm A-V-\\Omega").scale(0.2).shift(UP * 0.35)

        # 表盘外框
        box_width = 2 * (max(-vgGrads.get_left()[0], vgGrads.get_right()[0]) + self.box_buff)
        box_height = vgGrads.get_height() + 2 * self.box_buff
        self.box = Rectangle(box_width, box_height).move_to([0, vgGrads.get_center()[1], 0])
        self.box.stretch(1.098, 1, about_point = self.box.get_top())

        # 机械调零旋钮
        mech_knob_radius = 0.05
        self.mech_knob = VGroup(
            Circle(radius = mech_knob_radius, stroke_color = WHITE), 
            Line(LEFT * mech_knob_radius, RIGHT * mech_knob_radius)
            )

        # 表盘底框
        coverCurve = VMobject()
        coverCurve.set_points([
            self.box.get_corner(DR) + DOWN * 0.15,
            self.box.get_bottom() + DOWN * 0.35,
            self.box.get_corner(DL) + DOWN * 0.15
            ])
        self.cover = VGroup(
            Line(self.box.get_corner(DL), self.box.get_corner(DL) + DOWN * 0.15),
            Line(self.box.get_corner(DR), self.box.get_corner(DR) + DOWN * 0.15),
            coverCurve
            )

        # 选择转盘
        vgSelects = self.initSelects().scale(0.4).align_to(self.cover.get_bottom(), UP)

        # 选择外框
        pfp1 = coverCurve.pfp(0.02)
        pfp2 = coverCurve.pfp(0.98)
        bottom = vgSelects.get_bottom()
        self.bottom_box = VMobject()
        self.bottom_box.set_points_as_corners([
            pfp1, [pfp1[0], bottom[1], 0] + DOWN * 0.1,
            [pfp2[0], bottom[1], 0] + DOWN * 0.1, pfp2
            ])

        self.add(
            vgGrads, 
            self.point, self.arrow, 
            self.tex, 
            self.box, self.mech_knob, self.cover, 
            vgSelects, self.bottom_box
            )

    @staticmethod
    def initOmegaGrads() -> VGroup:
        '''
        初始化欧姆表刻度
        返回包含 grad_omega_side, grad_omega_vg_txt, grad_omega 的 VGroup
        '''

        # 暴力列举刻度长度
        grad_len_list = (
            1,      # 0
            0, 0, 0, 0,
            0, 
            0, 0, 0, 0,
            0,      # 10
            0, 0, 0.6, 0,
            0, 
            0, 0.6, 0, 0,
            0.6,    # 20
            0, 0, 0.6, 0,
            1, 
            0.6, 0, 0.6, 0,         # 26~33
            0.6,      # 30
            0, 0.6, 0, 1,
            0.6, 
            1, 0.6, 0.6, 0.6,
            0.6,      # 40
            1, 0.6, 0.6, 0.6,
            0.6, 
            1, 0.6, 0.6, 0.6,
            0.6,      # 50
            1, 0.6, 0.6, 0.6,
            0.6, 
            1, 0.6, 0.6, 0.6,
            0.6,      # 60
            1, 0.6, 0.4, 0.6,
            0.4, 
            0.6, 0.4, 0.6, 0.4,
            1,      # 70
        )
        grad_omega = PhyArrowEquip(
            arrow_enabled = False, grad_cnt = 7, grad_down = False, 
            grad_len_fn = lambda i: grad_len_list[i], 
            grad_fn = rush_into
            )
        grad_omega.grads[26:34].rotate(-0.7 * DEGREES, about_point = ORIGIN)

        # 刻度侧边物件
        # 包含"Ω"符号及其线条
        grad_omega_sideline = VMobject(stroke_width = 1.6)
        grad_omega_sideline.set_points_as_corners([LEFT * 0.1, LEFT, LEFT + 0.3 * UL]).scale(0.15)\
            .next_to(grad_omega.arc.get_end(), DR, buff = 0)
        grad_omega_sidetex = Tex("\\Omega").scale(0.2).next_to(grad_omega_sideline.get_points()[1], UP, buff = 0.025)
        grad_omega_side = VGroup(grad_omega_sideline, grad_omega_sidetex)

        # 暴力列举刻度数字
        def create_txt(ind, txtstr, txtclass = PhyMultiEquip.NumTxt, buff = 0.05):
            line = grad_omega.grads[ind]
            point = line.get_start()
            rad = np.arctan2(point[1] - line.get_end()[1], point[0] - line.get_end()[0]) - PI / 2
            offset = point - line.get_end()
            txt = txtclass(txtstr).move_to(point + buff / np.sqrt(offset[0]**2 + offset[1]**2) * offset)
            txt.rotate(rad)
            return txt
        grad_omega_vg_txt = VGroup(
            Tex('\\infty').scale(0.15).next_to(grad_omega.grads[0].get_center(), DL, buff = 0.02),
            create_txt(13, '1k', buff = 0.09),
            create_txt(25, '100'),
            create_txt(34, '50'),
            create_txt(36, '40'),
            create_txt(41, '30'),
            create_txt(46, '20'),
            create_txt(51, '15'),
            create_txt(56, '10'),
            create_txt(61, '5'),
            create_txt(70, '0')
            )
        grad_omega_vg_txt[3].shift(LEFT * 0.01)
        grad_omega_vg_txt[4].shift(UR * 0.01)

        return VGroup(grad_omega_side, grad_omega_vg_txt, grad_omega)

    @staticmethod
    def initDCGrads():
        '''
        初始化直流刻度
        返回包含 grad_DC_side, grad_DC_vg_txt, grad_DC 的 VGroup
        '''

        # 刻度
        grad_DC = PhyArrowEquip(
            arc_radius = 0.92, numtxtclass = PhyMultiEquip.NumTxt,
            arrow_enabled = False, grad_cnt = 5, grad_up = False, grad_half_len = 0.05
            )
        
        # 刻度侧边物件
        grad_DC_sideline = VMobject(stroke_width = 1.6)
        grad_DC_sideline.set_points_as_corners([LEFT * 0.6, ORIGIN, UR * 0.2]).scale(0.15)\
            .next_to(grad_DC.arc.get_start(), DL, buff = 0)
        grad_DC_sidetex = Tex("\\bar{\\tilde{}}").scale(0.4).next_to(grad_DC_sideline.get_points()[1], DOWN, buff = 0.025)
        grad_DC_side = VGroup(grad_DC_sideline, grad_DC_sidetex)
        
        # 刻度文字
        grad_DC_vg_txt = VGroup(VGroup(), VGroup(), VGroup())
        grad_DC.generate_nums((0, 5), 50, -1, 0.02, grad_DC_vg_txt[0])
        grad_DC.generate_nums((0, 5), 10, -1, 0.08, grad_DC_vg_txt[1])
        grad_DC.generate_nums((0, 5), 2, -1, 0.14, grad_DC_vg_txt[2])

        return VGroup(grad_DC_side, grad_DC_vg_txt, grad_DC)

    @staticmethod
    def initACGrads():
        '''
        初始化交流刻度
        返回包含 grad_AC_side, grad_AC_vg_txt, grad_AC 的 VGroup
        '''

        # 刻度
        grad_AC = PhyArrowEquip(
            arc_radius = 0.64,
            arrow_enabled = False, grad_cnt = 4, grad_up = False, grad_half_len = 0.05,
            grad_fn = lambda t: t**1.05
            )
        
        # 刻度侧边物件
        grad_AC_sideline = VGroup(stroke_width = 1.6)
        grad_AC_sideline.set_points_as_corners([UR * 0.16, ORIGIN, LEFT * 0.6, DL * 0.6]).scale(0.15)\
            .next_to(grad_AC.arc.get_start(), DL, buff = 0)
        grad_AC_sidetex = Tex("", "\\rm V", "\\sim").scale(0.15)
        grad_AC_sidetex[1].stretch(0.5, 1).next_to(grad_AC_sidetex[0], DOWN, buff = 0.02)
        grad_AC_sidetex.next_to(grad_AC_sideline.get_points()[4], DOWN, buff = 0.025)
        grad_AC_side = VGroup(grad_AC_sideline, grad_AC_sidetex)
        
        # 暴力列举刻度数字
        def create_txt(ind, txtstr, txtclass = PhyMultiEquip.NumTxt, buff = 0.09):
            line = grad_AC.grads[ind]
            point = line.get_end()
            rad = np.arctan2(line.get_start()[1] - point[1], line.get_start()[0] - point[0]) - PI / 2
            offset = point - line.get_start()
            txt = txtclass(txtstr).move_to(line.get_start() + buff / np.sqrt(offset[0]**2 + offset[1]**2) * offset)
            txt.rotate(rad)
            return txt
        grad_AC_vg_txt = VGroup(
            create_txt(0, '0'),
            create_txt(5, '0.5'),
            create_txt(10, '1'),
            create_txt(20, '1.5'),
            create_txt(30, '2'),
            create_txt(40, '2.5')
            )
        grad_AC_vg_txt[3].shift(LEFT * 0.01)
        grad_AC_vg_txt[4].shift(UR * 0.01)

        return VGroup(grad_AC_side, grad_AC_vg_txt, grad_AC)

    @staticmethod
    def initSelects():
        '''
        初始化选择转盘
        '''

        # 圆环
        circle_radius = 0.8
        circle1 = Circle(color = WHITE, radius = circle_radius, stroke_width = 3)
        circle2 = Circle(color = GREY, radius = 0.9 * circle_radius)
        circle = VGroup(circle1, circle2)
        
        # 指针
        arrow_body = VMobject(color = BLUE_A)
        arc1 = Arc.create_quadratic_bezier_points(8 * DEGREES, -4 * DEGREES)
        arc2 = Arc.create_quadratic_bezier_points(18 * DEGREES, 171 * DEGREES)
        arrow_body.set_points(arc1)
        arrow_body.add_points_as_corners([arc2[0]])
        arrow_body.append_points(arc2)
        arrow_body.add_points_as_corners([arc1[0]])
        arrow_body.scale(0.9 * circle_radius)
        arrow_tip = Line(RIGHT * 0.6 * circle_radius, RIGHT * 0.9 * circle_radius, color = BLUE_A)
        arrow = VGroup(arrow_body, arrow_tip)
        arrow.rotate(PhyMultiEquip.SWITCH_PER_ANGLE * 7)

        # 挡位
        vgSelectsSwitchLines = VGroup()
        for i in range(PhyMultiEquip.SWITCH_CNT):
            angle = i * PhyMultiEquip.SWITCH_PER_ANGLE
            x, y = np.cos(angle) * circle_radius, np.sin(angle) * circle_radius
            pos = np.array([x, y, 0])
            vgSelectsSwitchLines.add(Line(pos * 1.08, pos * 1.2, stroke_width = 3))
        left = vgSelectsSwitchLines.get_left()
        right = vgSelectsSwitchLines.get_right()
        top = vgSelectsSwitchLines.get_top()
        bottom = vgSelectsSwitchLines.get_bottom()
        # 调整左右挡位线条
        for i in (-2, -1, 1, 2):
            line: Line = vgSelectsSwitchLines[i]
            line.add_points_as_corners([np.array([right[0], line.get_end()[1], 0])])
        for i in (7, 8, 10):
            line: Line = vgSelectsSwitchLines[i]
            line.add_points_as_corners([np.array([left[0], line.get_end()[1], 0])])
        # 调整上下挡位线条
        line = vgSelectsSwitchLines[3]
        line.scale(2, about_point = line.get_start())
        line = vgSelectsSwitchLines[6]
        line.scale(2, about_point = line.get_start())
        for i in (3, 6):
            line: Line = vgSelectsSwitchLines[i]
            line.add_points_as_corners([np.array([line.get_end()[0], top[1], 0])])
        line = vgSelectsSwitchLines[11]
        line.scale(2.5, about_point = line.get_start())
        line = vgSelectsSwitchLines[12]
        line.scale(2, about_point = line.get_start())
        line = vgSelectsSwitchLines[15]
        line.scale(2, about_point = line.get_start())
        for i in (11, 12, 15):
            line: Line = vgSelectsSwitchLines[i]
            line.add_points_as_corners([np.array([line.get_end()[0], bottom[1], 0])])
        # 左右挡位文字
        vgSelectsSwitchTxtsRight = VGroup()
        for i, txtstr in zip((2, 1, 0, -1, -2), ('2.5', '10', '50', '250', '500')):
            line: Line = vgSelectsSwitchLines[i]
            txt = PhyMultiEquip.NumTxt(txtstr).scale(3)
            vgSelectsSwitchTxtsRight.add(txt.next_to(line.get_end(), RIGHT, 0.05))
        vgSelectsSwitchTxtsLeft = VGroup()
        for i, txtstr in zip((7, 8, 9, 10, 11), ('OFF', '250', '25', '2.5')):
            line: Line = vgSelectsSwitchLines[i]
            txt = PhyMultiEquip.NumTxt(txtstr).scale(3)
            vgSelectsSwitchTxtsLeft.add(txt.next_to(line.get_end(), LEFT, 0.05))
        # 上下挡位文字
        vgSelectsSwitchTxtsTop = VGroup()
        for i, txtstr in zip((3, 4, 5, 6), ('x1', 'x10', 'x100', 'x1k')):
            line: Line = vgSelectsSwitchLines[i]
            txt = PhyMultiEquip.NumTxt(txtstr).scale(3)
            vgSelectsSwitchTxtsTop.add(txt.next_to(line.get_end(), TOP, 0.02))
        vgSelectsSwitchTxtsTop[1].shift(RIGHT * 0.04)
        vgSelectsSwitchTxtsBottom = VGroup()
        for i, txtstr in zip((11, 12, 13, 14, 15), ('2.5', '10', '50', '250', '500')):
            line: Line = vgSelectsSwitchLines[i]
            txt = PhyMultiEquip.NumTxt(txtstr).scale(3)
            vgSelectsSwitchTxtsBottom.add(txt.next_to(line.get_end(), DOWN, 0.05))
        # 挡位文字
        vgSelectsSwitchTxts = VGroup(
            vgSelectsSwitchTxtsRight, vgSelectsSwitchTxtsLeft,
            vgSelectsSwitchTxtsTop, vgSelectsSwitchTxtsBottom
            )

        # 交流电压相关线条和文字
        line_AC = Line(vgSelectsSwitchTxtsRight.get_corner(UR) + UR * 0.05, vgSelectsSwitchTxtsRight.get_corner(DR) + DR * 0.05, stroke_width = 3)
        tex_AC = Tex("\\rm V", "\\sim")
        tex_AC[1].stretch(0.7, 1).next_to(tex_AC[0], DOWN, SMALL_BUFF)
        tex_AC.scale(0.5).next_to(line_AC, UL, SMALL_BUFF)
        vgAC = VGroup(line_AC, tex_AC)
        # 欧姆相关线条和文字
        line_omega = VMobject(stroke_width = 3)
        start = vgSelectsSwitchTxtsTop.get_corner(UL) + UL * 0.05
        end = vgSelectsSwitchTxtsTop.get_corner(UR) + UR * 0.05
        line_omega.set_points_as_corners([start + DOWN * 0.05 + LEFT * 0.02, start, end, end + DOWN * 0.05 + RIGHT * 0.02])
        tex_omega = Tex("\\Omega").scale(0.5).next_to(line_omega, LEFT, SMALL_BUFF)
        vgOmega = VGroup(line_omega, tex_omega)
        # 直流电流相关线条和文字
        vgTxtDCA = vgSelectsSwitchTxtsLeft[1:]
        line_DCA = Line(vgTxtDCA.get_corner(UL) + UL * 0.05, vgTxtDCA.get_corner(DL) + DL * 0.05, stroke_width = 3)
        tex_DCA = Tex("\\rm \\underline{mA}").scale(0.5).next_to(line_DCA, DOWN, SMALL_BUFF, LEFT)
        vgDCA = VGroup(line_DCA, tex_DCA)
        # 直流电压相关线条和文字
        line_DCV = Line(vgSelectsSwitchTxtsBottom.get_corner(DL) + DL * 0.05, vgSelectsSwitchTxtsBottom.get_corner(DR) + DR * 0.05, stroke_width = 3)
        tex_DCV = Tex("\\rm \\underline V").scale(0.5).next_to(line_DCV, RIGHT, SMALL_BUFF, DOWN)
        vgDCV = VGroup(line_DCV, tex_DCV)

        # 相关线条和文字
        vgLinesAndTexs = VGroup(vgAC, vgOmega, vgDCA, vgDCV)
        
        return VGroup(circle, arrow, vgSelectsSwitchLines, vgSelectsSwitchTxts, vgLinesAndTexs)

class PhyEquipR(VMobject):
    def __init__(self, width = 1.7, height = 0.6, buff = 0.1, **kwargs):
        super().__init__(**kwargs)

        xy = np.array([width / 2, height / 2, 0])
        self.set_points_as_corners([UL * xy, UR * xy, DR * xy, DL * xy, UL * xy])
        xy -= [buff, buff, 0]
        self.add_points_as_corners([UL * xy, DL * xy, DR * xy, UR * xy, UL * xy])
        self.set_stroke(width = 0).set_fill(opacity = 1)

class PhyElecLine(VMobject):
    def __init__(self, start = LEFT, end = RIGHT, width = 0.1, **kwargs):
        super().__init__(**kwargs)

        width /= 2
        rot = PI / 2 + np.arctan2(end[1] - start[1], end[0] - start[0])
        delta = [width * np.cos(rot), width * np.sin(rot), 0]
        self.set_points_as_corners([start + delta, end + delta, end - delta, start - delta, start + delta])
        self.set_stroke(width = 0).set_fill(opacity = 1)


class PhyHeaderTestScene(Scene):
    def construct(self):
        mobj = PhyMultiEquip().scale(3)
        self.add(mobj)
        self.play(mobj.arrow_offset.animate.set_value(1))
        
        # mobj = PhyArrowEquip("A", grad_cnt = 4, grad_zero_offset = 1, grad_fn = rush_into).scale(2)
        # self.add(mobj)
        # self.wait(0.5)
        # self.play(mobj.arrow_offset.animate.increment_value(18), run_time = 1.5)

        # self.add(PhyElecLine(UP, DOWN).shift(LEFT * 3), PhyEquipR(), PhyEquipTxt("G").shift(RIGHT * 3).insert_n_curves(8))

        # mobj = PhyMaterialEquip("A", wire_base_color = (BLACK, "#ff4444", "#ff4444"), wire_base_txt = ("|-|", "0.6", "3"), grad_zero_offset = -1, grad_up_num_step = 1, grad_down_num_step = 0.2).scale(2)
        # self.add(mobj)
        # self.wait(0.5)
        # self.play(mobj.arrow_offset.animate.increment_value(22), run_time = 1.5)
        # self.wait(0.5)

