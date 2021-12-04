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
        def __init__(self, txt, **kwargs):
            super().__init__(txt, font = "Noto Sans Thin")
            self.scale(0.6)
    class NumTxt(Text):
        def __init__(self, txt, **kwargs):
            super().__init__(txt, font = "Noto Sans Thin")
            self.scale(0.3)
    
    CONFIG = {
        "txtclass" : Txt,
        "numtxtclass" : NumTxt,
        "line_width" : 1,
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
            self.generate_nums(self.grad_up_range, self.grad_up_step, 1, self.up_nums)
        if self.grad_down_step != None:
            self.generate_nums(self.grad_down_range, self.grad_down_step, -1, self.down_nums)
        
        self.wo_arrow = VGroup(self.txt, self.arc, self.grads, self.up_nums, self.down_nums)

        # 指针
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

        self.add(self.wo_arrow, self.point, self.arrow)
    
    def grad_rot(self, ind):
        return self.arc_start_angle - self.grad_fn(ind / self.grad_total_cnt) * self.arc_rad
    def numstr(self, val):
        result = '%.1f' % val
        if result.endswith('.0'):
            result = result[:len(result) - 2]
        return result

    def generate_nums(self, g_range, step, sign, vg):
        for i in range(g_range[0], g_range[1] + 1):
            rot = self.grad_rot(i * 10)
            direction = RIGHT * np.cos(rot) + UP * np.sin(rot)
            txt = self.numstr(step * (i - self.grad_zero_offset))
            num = self.numtxtclass(txt)
            num.move_to(direction * (self.arc_radius + sign * (self.grad_half_len + num.get_height() / 2 + self.grad_num_buff)))
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
        "box_buff": 0.1
    }

    class NumTxt(Text):
        def __init__(self, txt, **kwargs):
            super().__init__(txt, font = "Noto Sans Thin")
            self.scale(0.12)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        self.grad_omega = PhyArrowEquip(
            grad_cnt = 7, grad_down = False, 
            grad_len_fn = lambda i: grad_len_list[i], 
            grad_fn = rush_into
            )
        self.grad_omega.grads[26:34].rotate(-0.7 * DEGREES, about_point = ORIGIN)
        grad_omega_sideline = VMobject(stroke_width = 1.6)
        grad_omega_sideline.set_points_as_corners([LEFT * 0.1, LEFT, LEFT + 0.3 * UL]).scale(0.15)\
            .next_to(self.grad_omega.arc.get_end(), DR, buff = 0)
        grad_omega_sidetex = Tex("\\Omega").scale(0.2).next_to(grad_omega_sideline.get_points()[1], UP, buff = 0.025)
        self.grad_omega_side = VGroup(grad_omega_sideline, grad_omega_sidetex)
        def create_txt(ind, txtstr, txtclass = self.NumTxt, buff = 0.05):
            line = self.grad_omega.grads[ind]
            point = line.get_start()
            rad = np.arctan2(point[1] - line.get_end()[1], point[0] - line.get_end()[0]) - PI / 2
            offset = point - line.get_end()
            txt = txtclass(txtstr).move_to(point + buff / np.sqrt(offset[0]**2 + offset[1]**2) * offset)
            txt.rotate(rad)
            return txt
        self.grad_omega_vg_txt = VGroup(
            Tex('\\infty').scale(0.15).next_to(self.grad_omega.grads[0].get_center(), DL, buff = 0.02),
            create_txt(13, '1k', buff = 0.08),
            create_txt(25, '100', buff = 0.04),
            create_txt(34, '50', buff = 0.04),
            create_txt(36, '40'),
            create_txt(41, '30'),
            create_txt(46, '20'),
            create_txt(51, '15'),
            create_txt(56, '10'),
            create_txt(61, '5'),
            create_txt(70, '0')
            )
        vg_grad_omega = VGroup(self.grad_omega_side, self.grad_omega_vg_txt, self.grad_omega)

        vgGrads = VGroup(vg_grad_omega)

        box_width = 2 * (max(-vgGrads.get_left()[0], vgGrads.get_right()[0]) + self.box_buff)
        box_height = vgGrads.get_height() + 2 * self.box_buff
        self.box = Rectangle(box_width, box_height).move_to([0, vgGrads.get_center()[1], 0])

        self.add(vgGrads, self.box)

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
        
