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

# 未测试
class PhyMaterialEquip(VGroup):
    def __init__(self, txt = "", arc_radius = 1, arc_rad = PI / 2, grad_half_len = 0.1):
        self.txt = Text(txt).scale(0.2).move_to([0, arc_radius / 2, 0])
        arc_start_angle = (PI - arc_rad) / 2
        self.arc = Arc(arc_start_angle, arc_rad, radius = arc_radius)
        self.grads = VGroup()
        for i in range(0, 41):
            rot = arc_start_angle + (40 - i) / 40 * arc_rad
            x = np.cos(rot) * arc_radius
            y = np.sin(rot) * arc_radius
            ghl = grad_half_len * (0.5 if i % 10 == 0 else (0.75 if i % 5 == 0 else 1))
            xoffset = np.cos(rot) * ghl
            yoffset = np.sin(rot) * ghl
            self.grads.add(Line([x + xoffset, y + yoffset, 0], [x - xoffset, y - yoffset, 0]))

        super().__init__(self.txt, self.arc, self.grads)


class PhyHeaderTestScene(Scene):
    def construct(self):
        a = PhyEquipLight()
        b = PhyEquipTxt("V").next_to(a, LEFT)
        c = PhyEquipTxt("A").next_to(a, RIGHT)
        self.add(a, b, c)