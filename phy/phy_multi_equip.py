import sys
sys.path.append('.')
from manimlib import *
from phy.phy_header import *

class EquipLine(VGroup):
    class Socket(VGroup):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_socket_pos(self):
            return self[1].get_center()
        def move_socket_to(self, target):
            delta = target - self.get_socket_pos()
            self.shift(delta)
            return self
        def rotate_socket(self, deg):
            self.rotate(deg, about_point = self.get_socket_pos())
            return self
    
    class Probe(VGroup):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def get_probe_pos(self):
            return self[0].get_start()
        def get_probe_end(self):
            return self[1].get_points()[6]
        def move_probe_to(self, target):
            delta = target - self.get_probe_pos()
            self.shift(delta)
            return self
        def rotate_probe(self, deg):
            self.rotate(deg, about_point = self.get_probe_pos())
            return self

    def __init__(self, color1 = RED, color2 = RED_E, color3 = GREY_A):
        self.block_line_updater = True

        self.line = VMobject().set_stroke(color1, width = 7)
        self.socketHead = VMobject()
        self.socketHead.set_points_as_corners([  # [5]
            [0.2, -0.2, 0], [-0.2, -0.2, 0], [-0.2, 0.2, 0],
            [0.2, 0.2, 0], [0.4, 0.15, 0],
            [0.4, 0, 0], 
            [0.4, -0.15, 0], [0.2, -0.2, 0]
        ]).scale(0.8).set_stroke(color1).set_fill(color2, 1)
        self.probeHead1 = VMobject()
        self.probeHead1.set_points_as_corners([
            [0, 0, 0], [0.1, 0.02, 0], [0.8, 0.05, 0],
            [0.8, -0.05, 0], [0.1, -0.02, 0], [0, 0, 0]
        ]).set_stroke(opacity = 0).set_fill(color3, 1)
        self.probeHead2 = VMobject()
        self.probeHead2.set_points_as_corners([  # [2]
            [0.8, 0.08, 0], [3, 0.12, 0],
            [3, 0, 0],
            [3, -0.12, 0], [0.8, -0.08, 0],
            [0.8, 0.08, 0]
        ]).set_stroke(color1).set_fill(color2, 1)
        self.socketDot = Dot(radius = 0.02, color = color1).set_opacity(1)

        self.probe = self.Probe(self.probeHead1, self.probeHead2)
        self.socket = self.Socket(self.socketHead, self.socketDot)
    
        super().__init__(self.socketHead, self.probe, self.socket, self.line)
        self.add_updater(self.lineUpdater)
        self.set_stroke(width = 3)

    def lineUpdater(self, _):
        if self.block_line_updater:
            return
        self.update_line()
    
    def update_line(self):
        socketTarget = self.socketHead.get_points()[15]
        socketOffset = socketTarget - self.socketDot.get_center()
        socketOffset /= np.sqrt(sum([v**2 for v in socketOffset]))
        socketExtend = socketTarget + socketOffset * 5
        probeTarget = self.probeHead2.get_points()[6]
        probeOffset = probeTarget - self.probeHead1.get_points()[1]
        probeOffset /= np.sqrt(sum([v**2 for v in probeOffset]))
        probeExtend = probeTarget + probeOffset * 5
        avgExtend = (socketExtend + probeExtend) / 2
        self.line.set_points([
            socketTarget, socketExtend, avgExtend,
            avgExtend, probeExtend, probeTarget
            ])
        self.line.set_stroke(width = 7)
        return self

class EquipLine2(EquipLine):
    def __init__(self, color1 = RED, color2 = RED_E, color3 = GREY_A):
        super().__init__(color1, color2, color3)
        self.socket.scale(1e-5).set_opacity(0)

class Battery(VGroup):
    CONFIG = {
        "line_po_len": 1,
        "line_ne_len": 0.5,
        "line_buff": 0.2,
        "line_config": {}
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.linePo = Line(ORIGIN, DOWN * self.line_po_len, **self.line_config)
        self.lineNe = Line(ORIGIN, DOWN * self.line_ne_len, **self.line_config)
        self.add(self.lineNe, self.linePo).arrange(RIGHT, buff = self.line_buff)


class OpeningScene(Scene):
    def construct(self):
        txt = Text("【物理】多用电表的使用与原理", t2c = { "【物理】": BLUE })
        self.play(DrawBorderThenFill(txt))
        self.wait()
        self.play(FadeOut(txt))

class EquipScene(Scene):
    def construct(self):
        # 显示多用电表
        equ = PhyMultiEquip().scale(2.5)
        self.play(*map(Write, (VGroup(equ[0:4], equ[5], equ[7]), VGroup(equ[4], equ[6], equ[8]))), run_time = 2)
        self.wait()

        def highlight(l):
            self.play(*[mobj.animate.set_color(ORANGE) for mobj in l], run_time = 0.5)
            self.wait(0.5)
            self.play(*[mobj.animate.set_color(WHITE) for mobj in l], run_time = 0.5)

        # 高亮电阻档位
        gOmega = Group(equ[0][0], equ[7][0][2][3:7], equ[7][0][3][2], equ[7][0][4][1])
        highlight(gOmega)
        # 高亮直流电流档位
        gDCA = Group(equ[0][1], equ[7][0][2][8:11], equ[7][0][3][1][1:], equ[7][0][4][2])
        highlight(gDCA)
        # 高亮直流电压档位
        gDCV = Group(equ[0][1], equ[7][0][2][11:16], equ[7][0][3][3], equ[7][0][4][3])
        highlight(gDCV)
        # 高亮交流电压档位
        gACV = Group(equ[0][2], equ[7][0][2][0:3], equ[7][0][2][16:18], equ[7][0][3][0], equ[7][0][4][0])
        highlight(gACV)

        self.wait()

        # 高亮转盘和表盘
        equCircle = equ[7][0][0]
        equGrads = equ[0]
        equCircle.save_state()
        self.play(equCircle.animate.set_color(YELLOW))
        self.wait()
        equGrads.save_state()
        self.bring_to_back(equGrads)
        self.play(equGrads.animate.set_color(YELLOW))
        self.wait()
        self.play(*[mobj.animate.restore() for mobj in [equCircle, equGrads]])

class UseScene(Scene):
    def construct(self):
        frame: CameraFrame = self.camera.frame

        equ = PhyMultiEquip().scale(2.5)
        self.add(equ)

        el1 = EquipLine()
        el1.socket.move_socket_to(equ[7][1][1].get_center()).rotate_socket(-45 * DEGREES)
        el1.probe.move_probe_to(el1.socket.get_socket_pos() + RIGHT + UP * 3).rotate_probe(-30 * DEGREES)
        el1.update_line()

        el2 = EquipLine(GREY_D, "#333333", GREY_A)
        el2.socket.move_socket_to(equ[7][1][2].get_center()).rotate_socket(-45 * DEGREES)
        el2.probe.move_probe_to(el2.socket.get_socket_pos() + RIGHT + UP * 3).rotate_probe(-30 * DEGREES)
        el2.update_line()

        self.wait()
        el1.generate_target()
        el1.scale(1.2, about_point = el1.socket.get_socket_pos()).set_opacity(0)
        el2.generate_target()
        el2.scale(1.2, about_point = el2.socket.get_socket_pos()).set_opacity(0)
        self.play(
            AnimationGroup(
                MoveToTarget(el1), 
                MoveToTarget(el2), 
                lag_ratio = 0.5)
            )
        el1.block_line_updater = False
        el2.block_line_updater = False

        self.wait()
        self.play(equ.arrow_offset.animate.set_value(0.1), run_time = 0.2)
        self.play(equ.arrow_offset.animate.set_value(-0.1), run_time = 0.4)
        self.play(equ.arrow_offset.animate.set_value(0), run_time = 0.2)

        txtMechKnob = VGroup(
            Text("机械调零", color = GREY_A), 
            Triangle().set_fill(GREY_A, opacity = 1).set_stroke(opacity = 0).rotate(-PI / 2)
            )
        txtMechKnob[1].set_height(txtMechKnob[0].get_height()).next_to(txtMechKnob[0], buff = SMALL_BUFF)
        txtMechKnob.scale(0.5).next_to(equ.mech_knob, LEFT, buff = SMALL_BUFF)
        # txtMechKnob.set_y(equ.arrow.get_center()[1])
        circle = Circle().set_stroke(YELLOW, opacity = 1).set_fill(opacity = 0)
        circle.surround(equ.mech_knob)

        self.wait()
        frame.save_state()
        self.play(frame.animate.shift(UP).scale(0.6), equ.arrow_offset.animate.set_value(0.1))
        self.play(FadeIn(txtMechKnob, RIGHT))
        self.wait(0.5)
        self.play(
            AnimationGroup(
                FadeIn(circle, scale = 0.8, run_time = 0.4),
                AnimationGroup(
                    equ.arrow_offset.animate.set_value(0),
                    equ.mech_knob.animate.rotate(20 * DEGREES)
                    ),
                lag_ratio = 0.3), 
            run_time = 1.3)
        self.play(FadeOut(circle, scale = 1.2, run_time = 0.4))
        self.wait(0.5)
        self.play(frame.animate.restore(), FadeOut(txtMechKnob))

        gDCA = Group(equ[0][1], equ[7][0][2][8:11], equ[7][0][3][1][1:], equ[7][0][4][2])
        self.wait(0.5)
        self.play(frame.animate.shift(DOWN).scale(0.8), *[mobj.animate.set_color(YELLOW) for mobj in gDCA])
        self.wait(0.5)
        self.play(Rotating(equ[7][0][1], 1 * equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center(), rate_func = smooth, run_time = 1))
        self.wait(1.5)
        self.play(frame.animate.shift(UP), gDCA[0][1][1:].animate.set_color(WHITE))

        phyPosi = Text("+").set_color(RED)
        phyNege = Text("-").set_color(BLUE)
        phyR = PhyEquipR()
        lineLeft = PhyElecLine()
        lineRight = PhyElecLine(end = RIGHT * 0.5)
        lineRight2 = PhyElecLine(end = RIGHT * 0.5)
        vgPhyR = VGroup(
            phyPosi, 
            VGroup(lineLeft, phyR, lineRight, lineRight2).arrange(buff = 0),
            phyNege
            ).arrange()\
            .scale(0.4).next_to(equ.box, buff = MED_LARGE_BUFF)
        self.wait(0.5)
        self.play(frame.animate.shift(RIGHT * 2.5), Write(vgPhyR), run_time = 1.5)
        lineRight2.generate_target()
        lineRight2.target.shift(RIGHT)
        el1.probe.save_state()
        el2.probe.save_state()
        self.play(
            MoveToTarget(lineRight2), phyNege.animate.shift(RIGHT),
            el1.probe.animate.move_probe_to(lineRight.get_right()).rotate_probe(-65 * DEGREES),
            el2.probe.animate.move_probe_to(lineRight2.target.get_left()).rotate_probe(-55 * DEGREES),
            Animation(el1), Animation(el2),
            run_time = 2)

        arrow1 = Arrow(el1.probe.get_probe_pos(), el1.probe.get_probe_end(), stroke_width = 10).set_color(YELLOW)
        arrow2 = Arrow(el2.probe.get_probe_end(), el2.probe.get_probe_pos(), stroke_width = 10).set_color(YELLOW)
        self.wait(0.5)
        self.play(ShowCreation(arrow1))
        self.play(ShowCreation(arrow2))
        self.wait()
        self.play(*map(FadeOut, (arrow1, arrow2)))

        self.wait(0.5)
        self.play(equ.arrow_offset.animate.set_value(0.45))
        
        arc = equ[0][1][2].arc
        point = arc.pfp(0.45)
        self.wait(0.5)
        self.play(frame.animate.move_to(point + DOWN * 0.1).scale(0.2), run_time = 2)

        brace = Brace(Line(arc.pfp(0.40), arc.pfp(0.42)), UP, buff = 0.02)
        brace.stretch(0.2, 1, about_point = brace.get_bottom())
        tex = Tex("5").scale(0.2).next_to(brace, UP, 0.02)
        vgBrace = VGroup(brace, tex).rotate(6 * DEGREES, about_point = brace.get_corner(DR))
        self.wait(0.5)
        self.play(ShowCreation(vgBrace))

        texVal = Tex("\\rm 112mA", color = ORANGE).set_stroke(WHITE, 0.1).scale(0.2).next_to(frame.get_center(), buff = 0.02)
        self.wait(0.5)
        self.play(DrawBorderThenFill(texVal, stroke_width = 0.3))
        self.wait(2)

        texWrongVal = Tex("\\rm 112.5mA", color = RED_B).set_stroke(WHITE, 0.1).scale(0.2).next_to(texVal, DOWN, 0.04, LEFT)
        texValCopy = texVal.copy()
        cross = VGroup(Line(UR, DL), Line(UL, DR)).replace(texWrongVal, stretch = True).set_stroke(RED, 1)
        self.wait()
        self.play(Transform(texValCopy, texWrongVal, path_arc = -45 * DEGREES))
        self.play(ShowCreation(cross))
        self.wait()

        equ[7][0][1].rotate(-1 * equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center())
        self.play(
            AnimationGroup(
                frame.animate.restore(),
                el1.probe.animate.restore(), el2.probe.animate.restore(),
                Animation(el1), Animation(el2),
                equ.arrow_offset.animate.set_value(0),
                run_time = 2), 
            AnimationGroup(
                FadeOut(vgPhyR), 
                gDCA.animate.set_color(WHITE),
                *map(FadeOut, (vgBrace, texVal, texValCopy, cross)),
                run_time = 1.5),
            )
        self.wait()

class UseScene_EstimateScene(Scene):
    def construct(self):
        black = Rectangle(6, FRAME_HEIGHT * 0.7).set_fill(BLACK, 0.8).set_stroke(opacity = 0).to_edge(LEFT, 0)
        black.shift(black.get_width() * LEFT)
        self.add(black)
        self.play(black.animate.shift(RIGHT * black.get_width()), run_time = 1.5, rate_func = rush_from)

        txt1 = VGroup(Text("0.1"), Text("1"), Text("...")).scale(0.8).arrange(RIGHT, LARGE_BUFF).set_color(YELLOW_A)
        txt2 = Text("估读到下一位").scale(0.8)
        txt3 = VGroup(Text("0.2"), Text("2"), Text("0.5"), Text("5"), Text("...")).scale(0.8).arrange(RIGHT, LARGE_BUFF).set_color(YELLOW_A)
        txt4 = Text("估读到本位").scale(0.8)
        vg = VGroup(
            VGroup(txt1, txt2).arrange(DOWN, aligned_edge = LEFT),
            VGroup(txt3, txt4).arrange(DOWN, aligned_edge = LEFT),
            ).arrange(DOWN, aligned_edge = LEFT, buff = LARGE_BUFF).to_edge(LEFT, LARGE_BUFF * 2)
        txt1.shift(LEFT * 0.5)
        txt3.shift(LEFT * 0.5)

        self.play(Write(txt1))
        self.wait(0.5)
        self.play(FadeIn(txt2, scale = 1.1))
        self.wait()
        self.play(Write(txt3))
        self.wait(0.5)
        self.play(FadeIn(txt4, scale = 1.1))
        self.wait()
        
        self.play(*map(FadeOut, vg), run_time = 0.4)
        self.play(
            AnimationGroup(black.animate.shift(LEFT * black.get_width()), run_time = 1.5, rate_func = rush_into), 
            )

class UseVScene(Scene):
    def construct(self):
        frame: CameraFrame = self.camera.frame

        equ = PhyMultiEquip().scale(2.5)
        self.add(equ)

        el1 = EquipLine()
        el1.socket.move_socket_to(equ[7][1][1].get_center()).rotate_socket(-45 * DEGREES)
        el1.probe.move_probe_to(el1.socket.get_socket_pos() + RIGHT + UP * 3).rotate_probe(-30 * DEGREES)
        el1.update_line()

        el2 = EquipLine(GREY_D, "#333333", GREY_A)
        el2.socket.move_socket_to(equ[7][1][2].get_center()).rotate_socket(-45 * DEGREES)
        el2.probe.move_probe_to(el2.socket.get_socket_pos() + RIGHT + UP * 3).rotate_probe(-30 * DEGREES)
        el2.update_line()

        el1.block_line_updater = False
        el2.block_line_updater = False

        self.add(equ, el1, el2)

        gDCV = Group(equ[0][1], equ[7][0][2][11:16], equ[7][0][3][3], equ[7][0][4][3])
        gGradDC = equ[0][1]

        frame.save_state()

        self.wait()
        self.play(
            *[mobj.animate.set_color(YELLOW) for mobj in gDCV],
            gGradDC.animate.set_color(YELLOW),
            frame.animate.scale(0.8).shift(DOWN),
            Rotating(equ[7][0][1], 6 * equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center(), rate_func = smooth, run_time = 1),
            run_time = 2)

        self.wait(0.5)
        self.play(
            frame.animate.shift(UP),
            *[mobj.animate.set_color(WHITE) for mobj in [gGradDC[1][0], gGradDC[1][2]]],
            run_time = 2)

        phyPosi = Text("+").set_color(RED)
        phyNege = Text("-").set_color(BLUE)
        phyR = PhyEquipR()
        lineLeft = PhyElecLine()
        lineRight = PhyElecLine()
        vgPhyR = VGroup(
            phyPosi, 
            VGroup(lineLeft, phyR, lineRight).arrange(buff = 0),
            phyNege
            ).arrange()\
            .scale(0.4).next_to(equ.box, buff = MED_LARGE_BUFF)
        self.wait(0.5)
        self.play(frame.animate.shift(RIGHT * 2.5), Write(vgPhyR), run_time = 1.5)
        el1.probe.save_state()
        el2.probe.save_state()
        self.play(
            el1.probe.animate.move_probe_to(lineLeft.get_center()).rotate_probe(-65 * DEGREES),
            el2.probe.animate.move_probe_to(lineRight.get_center()).rotate_probe(-55 * DEGREES),
            Animation(el1), Animation(el2),
            run_time = 2)
        
        arrow1 = Arrow(el1.probe.get_probe_pos(), el1.probe.get_probe_end(), stroke_width = 10).set_color(YELLOW)
        arrow2 = Arrow(el2.probe.get_probe_end(), el2.probe.get_probe_pos(), stroke_width = 10).set_color(YELLOW)
        self.wait(0.5)
        self.play(ShowCreation(arrow1))
        self.play(ShowCreation(arrow2))
        self.wait()
        self.play(*map(FadeOut, (arrow1, arrow2)))

        self.wait(0.5)
        self.play(equ.arrow_offset.animate.set_value(0.476))

        arc = equ[0][1][2].arc
        point = arc.pfp(0.476)
        equ.arrow.save_state()
        self.wait(0.5)
        self.play(
            frame.animate.move_to(point + DOWN * 0.1).scale(0.2), 
            equ.arrow.animate.set_width(0.05),
            run_time = 2)

        brace = Brace(Line(arc.pfp(0.40), arc.pfp(0.42)), UP, buff = 0.02)
        brace.stretch(0.2, 1, about_point = brace.get_bottom())
        tex = Tex("1").scale(0.2).next_to(brace, UP, 0.02)
        vgBrace = VGroup(brace, tex).rotate(6 * DEGREES, about_point = brace.get_corner(DR))
        self.wait(0.5)
        self.play(ShowCreation(vgBrace))

        texVal = Tex("\\rm 23.8V", color = ORANGE).set_stroke(WHITE, 0.1).scale(0.2).next_to(frame.get_center(), buff = 0.02)
        self.wait(0.5)
        self.play(DrawBorderThenFill(texVal, stroke_width = 0.3))
        self.wait(2)

        self.play(
            *map(FadeOut, (texVal, vgBrace)),
            gGradDC[1][1].animate.set_color(WHITE),
            frame.animate.scale(4.7).move_to(arc.pfp(0.5) + DOWN * 2.8),
            Rotating(equ[7][0][1], -2 * equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center(), rate_func = smooth),
            run_time = 2)
        self.wait(0.5)
        self.play(gGradDC[1].animate.set_opacity(0.3))
        
        gradDC: PhyArrowEquip = gGradDC[2]
        steps = [0.5, 2, 10, 50, 100]
        nums = Group()
        for step in steps:
            vg = VGroup()
            gradDC.generate_nums((0, 5), step, -1, 0.02, vg)
            for mobj, align in zip(vg, gGradDC[1][0]):
                mobj.move_to(align).scale(3)
            nums.add(vg)
        nums.set_color(BLUE)
        selectPrev = equ[7][0][3][3][0]
        tmp = selectPrev.copy()
        self.wait()
        self.play(
            AnimationGroup(
                *map(lambda m: FadeIn(m.scale(1.5), scale = 2), nums[0]),
                selectPrev.animate.set_color(BLUE),
                run_time = 0.8),
            Transform(tmp, nums[0][-1].copy(), path_arc = -40 * DEGREES, run_time = 1),
            )
        self.remove(tmp)
        self.play(
            *[m.animate.scale(1 / 1.5) for m in nums[0]],
            run_time = 0.6)
        for i in range(1, len(nums)):
            prev = nums[i - 1]
            cur = nums[i]
            selectCur = equ[7][0][3][3][i]
            tmp = selectCur.copy()
            self.play(
                AnimationGroup(
                    *[ReplacementTransform(m1, m2.scale(1.5)) for m1, m2 in zip(prev, cur)],
                    selectPrev.animate.set_color(YELLOW),
                    selectCur.animate.set_color(BLUE),
                    Rotating(equ[7][0][1], equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center(), rate_func = smooth, run_time = 0.8),
                    run_time = 0.8),
                Transform(tmp, cur[-1].copy(), path_arc = -50 * DEGREES, run_time = 1)
                )
            self.remove(tmp)
            self.play(
                *[m.animate.scale(1 / 1.5) for m in cur],
                run_time = 0.6)
            selectPrev = selectCur

        self.wait()
        self.play(
            FadeOut(nums[-1]), selectPrev.animate.set_color(YELLOW),
            gradDC.animate.set_color(WHITE), 
            gGradDC[1].animate.set_opacity(1), 
            gGradDC[0].animate.set_color(WHITE),
            run_time = 0.8)
        self.play(
            AnimationGroup(
                FadeOut(vgPhyR),
                gDCV.animate.set_color(WHITE),
                run_time = 0.6),
            AnimationGroup(
                frame.animate.restore(),
                el1.probe.animate.restore(), el2.probe.animate.restore(),
                Animation(el1), Animation(el2),
                equ.arrow_offset.animate.set_value(0),
                run_time = 2)
            )
        self.wait()
        self.play(Rotating(equ[7][0][1], -8 * equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center(), rate_func = smooth, run_time = 1))
        self.wait()

class UseOmegaScene(Scene):
    def construct(self):
        frame: CameraFrame = self.camera.frame

        equ = PhyMultiEquip().scale(2.5)
        self.add(equ)

        el1 = EquipLine()
        el1.socket.move_socket_to(equ[7][1][1].get_center()).rotate_socket(-45 * DEGREES)
        el1.probe.move_probe_to(el1.socket.get_socket_pos() + RIGHT + UP * 3).rotate_probe(-30 * DEGREES)
        el1.update_line()

        el2 = EquipLine(GREY_D, "#333333", GREY_A)
        el2.socket.move_socket_to(equ[7][1][2].get_center()).rotate_socket(-45 * DEGREES)
        el2.probe.move_probe_to(el2.socket.get_socket_pos() + RIGHT + UP * 3).rotate_probe(-30 * DEGREES)
        el2.update_line()

        el1.block_line_updater = False
        el2.block_line_updater = False

        self.add(equ, el1, el2)

        frame.save_state()

        gOmega = Group(equ[0][0], equ[7][0][2][3:7], equ[7][0][3][2], equ[7][0][4][1])

        self.wait(0.5)
        self.play(*map(lambda m: m.animate.set_color(YELLOW), gOmega))

        def animate_set_color_group(group, col, run_time):
            self.play(
                AnimationGroup(
                    *map(lambda m: m.animate.set_color(col), group),
                    lag_ratio = 0.1
                ),
                run_time = run_time
            )
        
        self.wait(0.5)
        animate_set_color_group(gOmega[0][2].grads, BLUE, 1.5)
        self.wait(0.2)
        animate_set_color_group(gOmega[0][2].grads, YELLOW, 1.5)

        self.wait(0.5)
        animate_set_color_group(gOmega[2], BLUE, 1)
        self.wait(0.2)
        animate_set_color_group(gOmega[2], YELLOW, 1)

        self.bring_to_front(equ.arrow)

        self.wait()
        self.play(Rotating(equ[7][0][1], -3 * equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center(), rate_func = smooth, run_time = 1))

        self.wait()
        self.play(frame.animate.scale(0.6).shift(RIGHT * 2 + UP * 0.5))

        txtOmegaKnob = VGroup(
            Text("欧姆调零", color = GREY_A), 
            Triangle().set_fill(GREY_A, opacity = 1).set_stroke(opacity = 0).rotate(-PI / 2)
            )
        txtOmegaKnob[1].set_height(txtOmegaKnob[0].get_height()).rotate(-PI / 2).next_to(txtOmegaKnob[0], DOWN, SMALL_BUFF)
        txtOmegaKnob.scale(0.5).next_to(equ.omega_knob, UP, SMALL_BUFF)

        self.wait(0.5)
        self.play(FadeIn(txtOmegaKnob, DOWN * 0.5))

        el1.probe.save_state()
        el2.probe.save_state()

        self.wait(0.5)
        self.play(
            el2.probe.animate.rotate_probe(-5 * DEGREES), 
            el1.probe.animate.rotate_probe(70 * DEGREES).move_probe_to(el2.probe.get_probe_pos() + DOWN * 0.3),
            Animation(el1), Animation(el2),
            run_time = 1.6
        )
        self.play(equ.arrow_offset.animate.set_value(0.9), run_time = 1.2)

        circle = Circle().set_stroke(YELLOW, opacity = 1).set_fill(opacity = 0)
        circle.surround(equ.omega_knob)
        
        self.wait(0.5)
        self.play(
            AnimationGroup(
                FadeIn(circle, scale = 0.8, run_time = 0.4),
                AnimationGroup(
                    equ.arrow_offset.animate.set_value(1),
                    equ.omega_knob.animate.rotate(-20 * DEGREES)
                ),
                lag_ratio = 0.3
            ), 
            run_time = 1.3
        )
        self.play(FadeOut(circle, scale = 1.2, run_time = 0.4))
        self.wait(0.5)
        self.play(frame.animate.scale(1.3).shift(RIGHT * 0.5), FadeOut(txtOmegaKnob))

        lineLeft_ = PhyElecLine()
        lineRight_ = PhyElecLine()
        phyR = PhyEquipR()
        lineLeft = PhyElecLine()
        lineRight = PhyElecLine()
        vgPhyR = VGroup(
            lineLeft_,
            VGroup(lineLeft, phyR, lineRight).arrange(buff = 0),
            lineRight_
        ).arrange().scale(0.4).next_to(equ.box, buff = MED_LARGE_BUFF)
        el1RotAngle = (-70 - 60 - 20) * DEGREES
        el2RotAngle = (5 - 40) * DEGREES
        self.wait(0.5)
        self.play(
            Write(vgPhyR[1]), 
            el1.probe.animate.rotate_probe(el1RotAngle).move_probe_to(lineLeft.get_left()),
            el2.probe.animate.rotate_probe(el2RotAngle).move_probe_to(lineRight.get_right()),
            Animation(el1), Animation(el2),
            run_time = 2
        )

        crsLeft = VGroup(Line(UR, DL), Line(UL, DR)).scale(0.1).set_stroke(RED, 6).next_to(lineLeft, LEFT, SMALL_BUFF)
        crsRight = crsLeft.copy().next_to(lineRight, RIGHT, SMALL_BUFF)

        self.wait(0.5)
        self.play(FadeIn(lineLeft_, RIGHT), FadeIn(lineRight_, LEFT))
        self.play(
            *map(lambda m: FadeIn(m, scale = 1.2), (crsLeft, crsRight)),
            lineLeft_.animate.next_to(crsLeft, LEFT, SMALL_BUFF),
            lineRight_.animate.next_to(crsRight, RIGHT, SMALL_BUFF)
        )
        self.wait(0.5)
        self.play(*map(FadeOut, (lineLeft_, lineRight_, crsLeft, crsRight)), run_time = 0.6)

        self.wait()
        self.play(
            frame.animate.shift(LEFT * 2.2 + UP * 1.5).scale(0.4),
            equ.arrow_offset.animate.set_value(0.585),
            run_time = 2
        )

        texVal = Text("11", color = ORANGE).set_stroke(WHITE, 0.15).scale(0.3).move_to(frame.get_center() + UP * 0.5 + RIGHT * 0.2)
        
        self.wait(0.5)
        self.play(DrawBorderThenFill(texVal, stroke_width = 0.15))
        
        radius = np.sqrt(
            sum(
                [
                    v**2 for v in
                    (equ[0][0][2].arc.get_start() - equ.point.get_center())
                ]
            )
        )
        center = equ.point.get_center()
        arc1 = VMobject()
        arc2 = VMobject()
        aph = 0.61
        arcAngle = 90 * DEGREES
        aphAngle = aph * arcAngle
        arcStart = 135 * DEGREES
        arcCenter = arcStart - aphAngle

        points1 = Arc.create_quadratic_bezier_points(-aphAngle, arcStart) * 1.02 * radius
        points2 = Arc.create_quadratic_bezier_points(aphAngle, arcCenter) * 0.98 * radius
        arc1.set_points(points1)
        arc1.add_points_as_corners([points1[-1], points2[0]])
        arc1.append_points(points2)
        arc1.add_points_as_corners([points2[-1], points1[0]])
        arc1.shift(center).set_stroke(width = 0).set_fill(BLUE_D, 0.6)

        points1 = Arc.create_quadratic_bezier_points(aphAngle - arcAngle, arcCenter) * 1.02 * radius
        points2 = Arc.create_quadratic_bezier_points(arcAngle - aphAngle, arcStart - arcAngle) * 0.98 * radius
        arc2.set_points(points1)
        arc2.add_points_as_corners([points1[-1], points2[0]])
        arc2.append_points(points2)
        arc2.add_points_as_corners([points2[-1], points1[0]])
        arc2.shift(center).set_stroke(width = 0).set_fill(BLUE_B, 0.6)

        self.wait()
        self.play(
            Write(arc1, stroke_width = 0.2, stroke_color = BLUE_D),
            Write(arc2, stroke_width = 0.2, stroke_color = BLUE_B),
            FadeOut(texVal, run_time = 0.6),
            frame.animate.restore().scale(0.4).shift(UP * 1.6),
            run_time = 1.5
        )

        def read_example_anim(arr, prev = None):
            for pair in arr:
                aph = pair[0]
                val = pair[1]
                rot = ((1 - aph) * 135 + aph * 45) * DEGREES
                direction = RIGHT * np.cos(rot) + UP * np.sin(rot)
                point = equ.grad_omega.arc.pfp(aph)
                txt = Text(val, color = BLUE).scale(0.3).move_to(point).rotate(rot - 90 * DEGREES).shift(direction * 0.25)
                self.wait(0.4)
                anim = AnimationGroup(equ.arrow_offset.animate.set_value(aph), FadeIn(txt), lag_ratio = 0.3)
                if prev == None:
                    self.play(anim)
                else:
                    self.play(anim, FadeOut(prev, run_time = 0.6))
                prev = txt
            return prev

        self.wait(0.5)
        prev = read_example_anim([[0.49, '15'], [0.256, '34'], [0.19, '45'], [0.09, '100']])
        self.wait(0.5)
        prev = read_example_anim([[0.635, '9.0'], [0.772, '4.3']], prev)
        
        self.wait(0.5)
        self.play(*map(FadeOut, (arc1, arc2)), run_time = 0.7)

        self.wait()
        self.play(frame.animate.scale(1.6).shift(DOWN), run_time = 1.5)

        vgResult = VGroup(
            VGroup(Text('4.3', color = BLUE), Text('×'), Text('10', color = YELLOW)).arrange().scale(0.7),
            VGroup(Tex('\\rightarrow'), Tex('43 \\Omega', color = GREEN)).arrange()
        ).scale(0.8).set_stroke(BLACK, 10, 0.5, True).arrange().next_to(equ.cover, UP, SMALL_BUFF)
        
        self.wait()
        self.play(Write(vgResult))

        el1.probe.generate_target()
        el2.probe.generate_target()
        el2.probe.target.restore().rotate(-5 * DEGREES)
        el1.probe.target.restore().rotate(70 * DEGREES).move_probe_to(el2.probe.target.get_probe_pos() + DOWN * 0.3)

        self.wait()
        self.play(
            frame.animate.shift(RIGHT * 1.5),
            equ.arrow_offset.animate.set_value(1.04),
            *map(FadeOut, (prev, vgResult, vgPhyR[1])),
            *map(MoveToTarget, (el1.probe, el2.probe)),
            *map(Animation, (el1, el2)),
            Rotating(equ[7][0][1], equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center(), rate_func = smooth, run_time = 2),
            run_time = 2
        )

        self.wait(0.5)
        self.play(
            AnimationGroup(
                FadeIn(circle, scale = 0.8, run_time = 0.4),
                AnimationGroup(
                    equ.arrow_offset.animate.set_value(1),
                    equ.omega_knob.animate.rotate(20 * DEGREES)
                ),
                lag_ratio = 0.6
            ), 
            run_time = 1.6
        )
        self.play(FadeOut(circle, scale = 1.2, run_time = 0.4))

        self.wait(1.5)
        self.play(
            el1.probe.animate.restore(), el2.probe.animate.restore(),
            Animation(el1), Animation(el2),
            frame.animate.shift(DOWN * 0.3),
            gOmega.animate.set_color(WHITE),
            equ.arrow_offset.animate.set_value(0),
            run_time = 1.5
        )

        self.wait(0.5)
        self.play(Rotating(equ[7][0][1], 2 * equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center(), rate_func = smooth, run_time = 1))
        
        self.wait()

class DiodeScene(Scene):
    def construct(self):
        frame: CameraFrame = self.camera.frame

        dots = Text('···')
        
        self.add(dots)
        self.wait()
        self.play(FadeOut(dots), run_time = 0.4)
        
        phyR = PhyEquipR()
        lineLeft = PhyElecLine()
        lineRight = PhyElecLine()
        vgPhyR = VGroup(lineLeft, phyR, lineRight).arrange(buff = 0).scale(0.4)

        el1 = EquipLine()
        el1.socket.move_socket_to(DOWN * 8).rotate_socket(-135 * DEGREES)
        el1.probe.move_probe_to(lineLeft.get_left()).rotate_probe(-110 * DEGREES)
        el1.update_line()

        el2 = EquipLine(GREY_D, "#333333", GREY_A)
        el2.socket.move_socket_to(DOWN * 8).rotate_socket(-45 * DEGREES)
        el2.probe.move_probe_to(lineRight.get_right()).rotate_probe(-70 * DEGREES)
        el2.update_line()

        frame.scale(0.7).shift(DOWN * 0.7)
        
        self.play(FadeIn(vgPhyR, DOWN * 0.5), FadeIn(el1, UP * 0.5), FadeIn(el2, UP * 0.5))

        arrow1 = Arrow(el1.probe.get_probe_pos(), el1.probe.get_probe_end(), stroke_width = 7).set_color(YELLOW)
        arrow2 = Arrow(el2.probe.get_probe_end(), el2.probe.get_probe_pos(), stroke_width = 7).set_color(YELLOW)
        self.wait(0.5)
        self.play(GrowArrow(arrow1))
        self.play(GrowArrow(arrow2))
        self.wait(0.5)
        self.play(*map(FadeOut, (arrow1, arrow2)), run_time = 0.8)

        arrowI = Arrow(lineRight.get_right() + UP * 0.5, lineLeft.get_left() + UP * 0.5, stroke_width = 4).set_color(BLUE)
        texI = Tex('I', color = BLUE).scale(0.8).next_to(arrowI, UP, SMALL_BUFF)
        self.wait(1.5)
        self.play(GrowArrow(arrowI), FadeIn(texI, UP * 0.5), run_time = 0.7)

        self.wait()
        self.play(phyR.animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(phyR.animate.set_color(WHITE))

        diode = PhyEquipDiode().move_to(phyR).rotate(PI).scale(0.5)

        self.wait()
        self.play(FadeIn(diode, DOWN * 0.5), FadeOut(phyR, DOWN * 0.5))

        arrowDiode1 = Arrow(RIGHT, LEFT, buff = 0).scale(0.7).next_to(diode, UP, SMALL_BUFF).set_color(PURPLE)
        texDiode1 = Tex('R\\rightarrow 0', color = PURPLE).scale(0.6).next_to(arrowDiode1, UP, SMALL_BUFF)
        vgDiode1 = VGroup(arrowDiode1, texDiode1)
        arrowDiode2 = Arrow(LEFT, RIGHT, buff = 0).scale(0.7).next_to(diode, DOWN, SMALL_BUFF).set_color(PURPLE)
        texDiode2 = Tex('R\\rightarrow +\\infty', color = PURPLE).scale(0.6).next_to(arrowDiode2, DOWN, SMALL_BUFF)
        vgDiode2 = VGroup(arrowDiode2, texDiode2)

        self.play(*map(lambda m: m.animate.shift(UP * 0.5), (arrowI, texI)), GrowArrow(arrowDiode1), FadeIn(texDiode1, LEFT * 0.5))
        self.wait(0.5)
        self.play(GrowArrow(arrowDiode2), FadeIn(texDiode2, RIGHT * 0.5))

        equ = PhyMultiEquip().scale(2.5).next_to(frame, LEFT, 0.02).shift(DOWN * 1.5)
        equ[7][0][1].rotate(-4 * equ.SWITCH_PER_ANGLE, about_point = equ[7][0][0].get_center())
        el1.block_line_updater = False
        el2.block_line_updater = False

        self.wait(1.5)
        self.play(equ.animate.shift(RIGHT * 2.5), frame.animate.shift(LEFT * 2.5), run_time = 1.6)
        self.wait(0.5)
        self.play(
            vgDiode2.animate.set_opacity(0.4), vgDiode1.animate.set_color(YELLOW),
            run_time = 1.5
        )
        self.play(equ.arrow_offset.animate.set_value(0.9), run_time = 1.5)
        self.wait()
        self.play(
            el1.probe.animate.rotate_probe(40 * DEGREES).move_probe_to(lineRight.get_right()),
            el2.probe.animate.rotate_probe(-40 * DEGREES).move_probe_to(lineLeft.get_left()),
            Animation(el1), Animation(el2),
            Rotating(arrowI, PI, rate_func = smooth, about_point = arrowI.get_center(), run_time = 1.5),
            vgDiode1.animate.set_opacity(0.4).set_color(PURPLE), vgDiode2.animate.set_opacity(1).set_color(YELLOW),
            run_time = 1.5
        )
        self.play(equ.arrow_offset.animate.set_value(0.01), run_time = 1.5)

        self.wait()

class PScene1(Scene):
    def construct(self):
        frame: CameraFrame = self.camera.frame
        txt = Text("原理").set_fill(opacity = 0).set_stroke(WHITE, 1).scale(4)
        equ = PhyMultiEquip().scale(2.5)

        self.add(txt)
        self.wait()
        self.play(
            FadeOut(txt, run_time = 0.6), FadeIn(equ),
            frame.animate.scale(0.7).shift(DOWN)
        )

        self.wait(0.5)
        self.play(Rotating(equ[7][0][1], -TAU, about_point = equ[7][0][0].get_center(), rate_func = smooth, run_time = 3))

        png = ImageMobject('assets/PME1_2_.png').set_height(2.6).move_to(frame.get_center())

        self.wait(0.5)
        self.play(FadeIn(png, UP * 0.5))
        self.wait(3)
        self.play(FadeOut(png, UP * 0.5))

        png = ImageMobject('assets/PRef.png').set_height(2.6).move_to(frame.get_center())

        self.wait(0.5)
        self.play(FadeIn(png, RIGHT * 0.3))
        self.wait(1.5)
        self.play(FadeOut(png, RIGHT * 0.3))

        self.wait(0.5)
        self.play(FadeOut(equ))
        
class PScene2(Scene):
    def construct(self):
        frame: CameraFrame = self.camera.frame
        
        line0 = PhyElecLine()
        batt = Battery(line_config = { 'stroke_width': 8 })
        line1 = PhyElecLine(ORIGIN, RIGHT)
        phyEquipG = PhyEquipTxt('G', radius = 0.6, scale_factor = 0.85)
        line2 = PhyElecLine(ORIGIN, RIGHT)
        dot = Dot(radius = 0.12)
        line3 = PhyElecLine(ORIGIN, RIGHT * 0.6)
        phyR = PhyEquipR()
        line4 = PhyElecLine()
        vg1 = VGroup(line0, batt, line1, phyEquipG, line2, dot, line3, phyR, line4).arrange(RIGHT, buff = 0)
        
        lineDL = PhyElecLine(UP, DOWN).next_to(line0, DOWN, 0, LEFT)
        lineDR = PhyElecLine(UP, DOWN).next_to(line4, DOWN, 0, RIGHT)
        lineMid1 = PhyElecLine(UP * 0.8, ORIGIN).next_to(dot, UP, 0)
        lineMid2 = PhyElecLine(ORIGIN, RIGHT * 1.6).next_to(lineMid1, UP, 0, LEFT)
        phyRMask = Rectangle().set_stroke(width = 0).set_fill(ORANGE, 0.5).set_height(phyR.get_height())
        pos = lineMid2.get_corner(UR)
        phyArrow = Arrow(pos, [pos[0], *phyR.get_top()[1:3]], buff = 0, stroke_width = 10).set_color(WHITE)

        def lineMid2_updater(_ = None):
            width = lineMid2.get_width()
            new_width = phyArrow.get_x() - lineMid1.get_left()[0]
            if new_width <= 0:
                return
            lineMid2.stretch(new_width / width, 0).next_to(lineMid1, UP, 0, LEFT)
        lineMid2_updater()
        def phyRMask_updater(_ = None):
            width = phyRMask.get_width()
            new_width = phyR.get_right()[0] - phyArrow.get_x()
            if new_width <= 0:
                return
            phyRMask.stretch(new_width / width, 0).next_to(phyR.get_right(), LEFT, 0)
        phyRMask_updater()

        texEr = VGroup(
            Tex('E', color = YELLOW), 
            Tex('r', color = ORANGE)
        ).arrange(aligned_edge = DOWN).next_to(batt, DOWN)
        texRg = Tex('R_g', color = ORANGE).next_to(phyEquipG, DOWN)
        texR = Tex('R', color = ORANGE).next_to(phyR, DOWN)
        circleRed = Circle(radius = 0.2, color = RED, stroke_width = 10, fill_opacity = 0).next_to(lineDL, DOWN, 0)
        circleBlack = Circle(radius = 0.2, color = GREY_D, stroke_width = 10, fill_opacity = 0).next_to(lineDR, DOWN, 0)

        el1 = EquipLine2()
        el1.socket.move_socket_to(circleRed.get_center()).rotate_socket(-110 * DEGREES)
        el1.probe.move_probe_to(DL * 3).rotate_probe(-110 * DEGREES)
        el1.update_line()
        el1.block_line_updater = False
        el2 = EquipLine2(GREY_D, "#333333", GREY_A)
        el2.socket.move_socket_to(circleBlack.get_center()).rotate_socket(-70 * DEGREES)
        el2.probe.move_probe_to(DR * 3).rotate_probe(-70 * DEGREES)
        el2.update_line()
        el2.block_line_updater = False

        frame.shift(DOWN)
        self.wait()
        self.play(
            FadeIn(Group(vg1, phyRMask), scale = 1.2),
            *map(lambda m: FadeIn(m, DOWN), (lineMid1, lineMid2, phyArrow)),
            *map(lambda m: FadeIn(m, UP), (lineDL, lineDR, texEr, texRg, texR, circleRed, circleBlack, el1, el2))
        )

        lineMid2.add_updater(lineMid2_updater)
        phyRMask.add_updater(phyRMask_updater)
        
        self.wait()
        self.play(
            AnimationGroup(
                *map(
                    lambda m: Indicate(m, scale_factor = 1.1),
                    (batt, phyEquipG, Group(phyR, phyRMask))
                ),
                lag_ratio = 2
            )
        )

        texEq1 = Tex(
            'E', '=', 'I_m', '\\cdot', '(', 
            'r', '+', 'R_g', '+', 'R', ')'
        ).shift(DOWN * 2 + LEFT)
        texEq1[0].set_color(YELLOW)
        texEq1[2].set_color(RED)
        texEq1[5].set_color(ORANGE)
        texEq1[7].set_color(ORANGE)
        texEq1[9].set_color(ORANGE)

        self.wait()
        self.play(
            AnimationGroup(
                frame.animate.shift(DOWN),
                AnimationGroup(
                    el1.probe.animate.move_probe_to(DOWN * 3 + RIGHT * 0.2).rotate_probe(-20 * DEGREES),
                    el2.probe.animate.move_probe_to(DOWN * 3 + LEFT * 0.2).rotate_probe(20 * DEGREES),
                    Animation(el1), Animation(el2),
                    run_time = 1.5
                ),
                lag_ratio = 0.2
            )
        )
        self.wait()
        self.play(Write(texEq1))
        self.play(ShowCreationThenDestruction(Underline(texEq1, color = YELLOW), run_time = 1.2))
        self.wait(0.5)
        self.play(ShowCreationThenDestruction(Underline(texEq1[2], color = YELLOW), run_time = 1.5))
        
        texRi = Tex('R_\\text{内}', color = ORANGE).next_to(texEq1[3], buff = SMALL_BUFF)
        texRiEq = VGroup(texRi.copy(), Tex('=')).arrange().next_to(texRi.get_left(), buff = 1.5)
        
        self.wait()
        self.play(
            AnimationGroup(
                texEq1[4:].animate.next_to(texRiEq),
                AnimationGroup(*map(lambda m: FadeIn(m, scale = 1.2), (texRi, texRiEq))),
                lag_ratio = 0.3
            )
        )

        lineRxLeft = PhyElecLine(ORIGIN)
        phyRx = PhyEquipR()
        lineRxRight = PhyElecLine(ORIGIN)
        vgPhyRx = VGroup(lineRxLeft, phyRx, lineRxRight).arrange(buff = 0).shift(DOWN * 4.5).scale(0.7)
        texRx = Tex('R_{\\mathsf x}', color = ORANGE).next_to(vgPhyRx, UP, SMALL_BUFF)

        self.wait()
        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeIn(vgPhyRx, scale = 1.2),
                    FadeIn(texRx, scale = 1.2)
                ),
                AnimationGroup(
                    el1.socket.animate.rotate_socket(-40 * DEGREES),
                    el2.socket.animate.rotate_socket(40 * DEGREES),
                    el1.probe.animate.move_probe_to(lineRxLeft.get_left()).rotate_probe(-30 * DEGREES),
                    el2.probe.animate.move_probe_to(lineRxRight.get_right()).rotate_probe(30 * DEGREES),
                    Animation(el1), Animation(el2),
                    run_time = 1.2
                ),
                lag_ratio = 0.1
            )
        )

        texEq2 = Tex(
            'E', '=', 'I', '\\cdot', '(', 'R_\\text{内}', '+', 'R_{\\mathsf x}', ')'
        ).next_to(texEq1, DOWN, aligned_edge = LEFT)
        texEq2[0].set_color(YELLOW)
        texEq2[2].set_color(RED_B)
        texEq2[5].set_color(ORANGE)
        texEq2[7].set_color(ORANGE)

        self.wait()
        self.play(Write(texEq2))
        self.play(ShowCreationThenDestruction(Underline(texEq2, color = YELLOW), run_time = 1.2))
        self.wait(0.5)
        self.play(ShowCreationThenDestruction(Underline(texEq2[2], color = YELLOW), run_time = 1.5))

        el1.block_line_updater = True
        el2.block_line_updater = True
        vgEq1Left = texEq1[:4]
        vgPhyRi = VGroup(texRiEq, texEq1[4:])

        self.wait()
        self.play(
            *map(
                FadeOut, (
                    texEr, texRg, texR,
                    vg1, lineDL, lineDR, dot, lineMid1, lineMid2, 
                    phyArrow, phyRMask, circleRed, circleBlack,
                    el1, el2, vgPhyRx, texRx
                )
            ),
            vgPhyRi.animate.set_opacity(0.5),
            frame.animate.shift(DOWN * 2),
            run_time = 1.2
        )

        texEq3Left = texEq2[2:].copy()
        texEq3Mid = Tex('=')
        texEq3Right = VGroup(vgEq1Left[2:].copy(), texRi.copy())
        vgTexEq3 = VGroup(texEq3Left, texEq3Mid, texEq3Right)
        texEq3Left.generate_target().next_to(texEq2, DOWN, LARGE_BUFF, LEFT)
        texEq3Mid.next_to(texEq3Left.target)
        texEq3Right.generate_target().next_to(texEq3Mid)

        self.wait()
        self.play(
            MoveToTarget(texEq3Left, path_arc = 60 * DEGREES),
            MoveToTarget(texEq3Right, path_arc = -60 * DEGREES), 
            FadeIn(texEq3Mid, scale = 1.2),
            run_time = 1.4
        )
        self.play(ShowCreationThenDestruction(Underline(vgTexEq3, color = YELLOW), run_time = 1.2))

        texEq4 = Tex('R_\\text{内}', '+', 'R_{\\mathsf x}', '=', '\\frac{I_m}{I}', 'R_\\text{内}')
        texEq4.next_to(texEq3Left.get_left(), buff = 0)
        texEq4[0].set_color(ORANGE)
        texEq4[2].set_color(ORANGE)
        texEq4[4][:2].set_color(RED)
        texEq4[4][3].set_color(RED_B)
        texEq4[5].set_color(ORANGE)
        transList = (
            (texEq3Left[3:6], texEq4[:3], 0),
            (texEq3Mid, texEq4[3], 0),
            (texEq3Right[0][0], texEq4[4][:2], 0),
            (texEq3Left[0], texEq4[4][3], 60 * DEGREES),
            (texEq3Right[1], texEq4[5], 0)
        )

        self.wait()
        self.play(
            *[FadeTransform(*v[:2], path_arc = v[2], run_time = 1.5) for v in transList],
            *[FadeOut(m, run_time = 0.6) for m in (texEq3Left[1:3], texEq3Left[-1], texEq3Right[0][-1])],
            FadeIn(texEq4[4][2], LEFT, run_time = 1.5)
        )

        texEq5 = Tex('R_{\\mathsf x}', '=', '\\frac{I_m}{I}', 'R_\\text{内}', '-', 'R_\\text{内}')
        texEq5.next_to(texEq4.get_left(), buff = 0)
        texEq5[0].set_color(ORANGE)
        texEq5[2][:2].set_color(RED)
        texEq5[2][3].set_color(RED_B)
        texEq5[3].set_color(ORANGE)
        texEq5[5].set_color(ORANGE)
        transList = (
            (texEq4[2:], texEq5[:4], 0),
            (texEq4[0], texEq5[-1], 90 * DEGREES),
            (texEq4[1], texEq5[-2], 90 * DEGREES)
        )

        self.play(*[FadeTransform(*v[:2], path_arc = v[2], run_time = 1.5) for v in transList])

        texEq6 = Tex('R_{\\mathsf x}', '=', 'R_\\text{内}', '(', '\\frac{I_m}{I}', '-', '1', ')')
        texEq6.next_to(texEq5.get_left(), buff = 0)
        texEq6[0].set_color(ORANGE)
        texEq6[2].set_color(ORANGE)
        texEq6[4][:2].set_color(RED)
        texEq6[4][3].set_color(RED_B)
        transList = (
            (texEq5[:2], texEq6[:2], 0),
            (texEq5[2], texEq6[4], 0),
            (texEq5[4], texEq6[5], 0),
            (texEq5[3], texEq6[2], 90 * DEGREES)
        )
        texEq5[5].generate_target().move_to(texEq6[2])

        self.play(
            *[FadeTransform(*v[:2], path_arc = v[2], run_time = 1.5) for v in transList],
            MoveToTarget(texEq5[5], run_time = 1.5, path_arc = 90 * DEGREES),
            *[FadeIn(m, RIGHT * 0.5, run_time = 1.5) for m in (texEq6[3], texEq6[6:])]
        )
        self.remove(texEq5[5])

        rect1 = BackgroundRectangle(texEq6[4][:2], buff = 0.1, color = YELLOW, stroke_width = 0, fill_opacity = 0.3)
        rect2 = BackgroundRectangle(texEq6[4][3], buff = 0.1, color = YELLOW, stroke_width = 0, fill_opacity = 0.3)
        rect3 = BackgroundRectangle(texEq6[0], buff = 0.1, color = YELLOW, stroke_width = 0, fill_opacity = 0.3)
        
        self.wait()
        self.play(
            AnimationGroup(
                AnimationGroup(frame.animate.move_to(texEq6).scale(0.5), run_time = 1.4),
                FadeIn(rect1, scale = 0.8),
                lag_ratio = 0.6
            )
        )
        self.wait()
        self.play(FadeOut(rect1, scale = 1.2), run_time = 0.7)
        self.wait(0.6)
        self.play(FadeIn(rect2, scale = 0.8), run_time = 0.7)
        self.wait()
        self.play(
            AnimationGroup(
                FadeOut(rect2, scale = 1.2), FadeIn(rect3, scale = 0.8),
                lag_ratio = 0.5
            ), 
            run_time = 0.7
        )
        self.wait()
        self.play(FadeOut(rect3, scale = 1.2))

        self.wait()
