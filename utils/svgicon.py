from manimlib import *

class IconServer(VGroup):   # 1 x 0.75
    def __init__(self):   
        super().__init__()

        a1 = Rectangle(1, 0.2)
        a2 = Line(ORIGIN, RIGHT * 0.3).next_to(a1.get_corner(UL), DR, 0.1)
        a3 = Circle(radius = 0.05).next_to(a1.get_right(), LEFT, 0.1)
        rect1 = VGroup(a1, a2, a3)
        rect2 = rect1.copy().next_to(rect1, DOWN, 0)
        rect3 = rect2.copy().next_to(rect2, DOWN, 0)
        self.add(rect1, rect2, rect3)

        top = VMobject()
        top.set_points_as_corners([rect1.get_corner(UL), rect1.get_corner(UL) + UR * 0.15, rect1.get_corner(UR) + UL * 0.15, rect1.get_corner(UR)])
        self.add(top)
        self.set_fill(opacity = 0).set_stroke(GREY_D, 2)
        self.move_to(ORIGIN)

class IconClient(VGroup):
    def __init__(self):
        super().__init__()

        a1 = Rectangle(0.3, 0.75)
        a2 = Line(ORIGIN, RIGHT * 0.25)
        a2_1 = a2.copy().next_to(a1.get_bottom(), UP, 0.05)
        a2_2 = a2.copy().next_to(a2_1, UP, 0.05)
        a3 = Rectangle(0.25, 0.05)
        a4 = Circle(radius = 0.05)
        left = VGroup(
            a1, a2.next_to(a1.get_top(), DOWN, 0.05), a3.next_to(a2, DOWN, 0.05),
            a2_1, a2_2, a4.next_to(a2_2, UP, 0.05)
            )
        self.add(left)

        b1 = Rectangle(0.6, 0.5)
        b2 = Rectangle(0.5, 0.4).move_to(b1)
        b3 = Rectangle(0.2, 0.075).next_to(b1, DOWN, 0)
        b4 = Rectangle(0.4, 0.075).next_to(b3, DOWN, 0)
        right = VGroup(b1, b2, b3, b4).next_to(left, RIGHT, 0.1, DOWN)
        self.add(right)

        self.set_fill(opacity = 0).set_stroke(GREY_D, 2)
        self.move_to(ORIGIN)
