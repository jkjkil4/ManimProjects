from manimlib import *


class PhyEquip(VMobject):
    CONFIG = {
        "radius": 1
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        circle_points = Arc.create_quadratic_bezier_points(TAU, n_components = 64)
        self.append_points(circle_points * 0.9)
        self.append_points(circle_points)
        self.scale(self.radius).set_stroke("#eeeeee", width = 1).set_fill(opacity = 1)

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
    def __init__(
        self, txt: str = "", 
        arc_radius = 1, arc_rad = PI / 2, grad_half_len = 0.1,
        grad_zero_offset = 0, grad_up_num_step = None, grad_down_num_step = None,
        grad_up_range = (-2, 2), grad_down_range = (-2, 2), grad_num_buff = 0.05
        ):
        # 中间文字
        self.txt = self.create_txt(txt).move_to([0, arc_radius / 2, 0])
        
        # 圆弧
        arc_start_angle = (PI - arc_rad) / 2
        self.arc = Arc(arc_start_angle, arc_rad, radius = arc_radius).set_stroke(width = 1.5)
        
        # 刻度
        self.grads = VGroup()
        for i in range(0, 41):
            rot = arc_start_angle + (40 - i) / 40 * arc_rad
            x = np.cos(rot) * arc_radius
            y = np.sin(rot) * arc_radius
            ghl = grad_half_len * (1 if i % 10 == 0 else (0.75 if i % 5 == 0 else 0.5))
            xoffset = np.cos(rot) * ghl
            yoffset = np.sin(rot) * ghl
            self.grads.add(Line([x + xoffset, y + yoffset, 0], [x - xoffset, y - yoffset, 0]).set_stroke(width = 1))
        
        # 刻度数字
        self.nums = VGroup()
        def numrot(offset):
            return PI / 2 - arc_rad * offset / 4
        def numstr(val):
            result = '%.1f' % val
            if result.endswith('.0'):
                result = result[:len(result) - 2]
            return result
        if grad_up_num_step != None:
            for i in range(grad_up_range[0], grad_up_range[1] + 1):
                rot = numrot(i)
                direction = RIGHT * np.cos(rot) + UP * np.sin(rot)
                text = numstr(grad_up_num_step * (i - grad_zero_offset))
                num = Text(text, font = "Noto Sans Thin").scale(0.3)
                num.move_to(direction * (arc_radius + grad_half_len + num.get_height() / 2 + grad_num_buff))
                num.rotate(rot - PI / 2)
                self.nums.add(num)
        if grad_down_num_step != None:
            for i in range(grad_down_range[0], grad_down_range[1] + 1):
                rot = numrot(i)
                direction = RIGHT * np.cos(rot) + UP * np.sin(rot)
                text = numstr(grad_down_num_step * (i - grad_zero_offset))
                num = Text(text, font = "Noto Sans Thin").scale(0.3)
                num.move_to(direction * (arc_radius - grad_half_len - num.get_height() / 2 - grad_num_buff))
                num.rotate(rot - PI / 2)
                self.nums.add(num)
        
        self.wo_arrow = VGroup(self.txt, self.arc, self.grads, self.nums)
        
        # 指针
        self.arrow_offset = ValueTracker(0)
        self.point = Dot().set_opacity(0)
        self.arrow = Line().set_color(BLUE).set_stroke(width = 2)
        def arrow_updater(m: Line):
            k = (20 - self.arrow_offset.get_value() - grad_zero_offset * 10) / 40
            rot = arc_start_angle + k * arc_rad
            radius = self.grads[20].get_y() - self.point.get_y() + grad_half_len / 2
            m.set_points_by_ends(self.point.get_center(), self.point.get_center() + [radius * np.cos(rot), radius * np.sin(rot), 0])
        self.arrow.add_updater(arrow_updater)

        super().__init__(self.wo_arrow, self.point, self.arrow)
    
    @staticmethod
    def create_txt(txt: str) -> Text:
        return Text(txt, font = "Noto Sans Thin").scale(0.6)

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
        self.add(PhyElecLine(UP, DOWN).shift(LEFT * 3), PhyEquipR(), PhyEquipTxt("G").shift(RIGHT * 3).insert_n_curves(8))

        # mobj = PhyMaterialEquip("A", wire_base_color = (BLACK, "#ff4444", "#ff4444"), wire_base_txt = ("|-|", "0.6", "3"), grad_zero_offset = -1, grad_up_num_step = 1, grad_down_num_step = 0.2).scale(2)
        # self.add(mobj)
        # self.wait(0.5)
        # self.play(mobj.arrow_offset.animate.increment_value(22), run_time = 1.5)
        # self.wait(0.5)
        
