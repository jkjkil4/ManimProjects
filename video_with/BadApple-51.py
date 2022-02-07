from manimlib import *

frame_path = 'C:\\Users\\jkjki\\Desktop\\Projects\\Other\\2022-1-15 Bad-Apple\\frame.png'
frame2_path = 'C:\\Users\\jkjki\\Desktop\\Projects\\Other\\2022-1-15 Bad-Apple\\frame2.png'

class CDRect(Rectangle):
    def __init__(self, ul, dr, **kwargs):
        super().__init__(dr[0] - ul[0], dr[1] - ul[1], **kwargs)
        self.move_to((ul + dr) / 2)

class Scene1(Scene):
    def construct(self):
        # img = ImageMobject(frame_path)
        # img.scale(FRAME_WIDTH / img.get_width())
        # self.add(img)
        # img.add_mouse_press_listner(lambda mobj, pos: print(mobj, pos))

        rect_buzzer = CDRect(np.array([-5.55, -2.99, 0]), np.array([-4.57, -3.85, 0]))
        rect_buzzer.set_stroke(YELLOW, 4).set_fill(opacity = 0)
        rect_lcd = CDRect(np.array([-2.40, -1.94, 0]), np.array([ 1.69, -3.31, 0]))
        rect_lcd.set_stroke(YELLOW, 4).set_fill(opacity = 0)

        txt_buzzer = Text("蜂鸣器").scale(0.6).next_to(rect_buzzer, UP, LARGE_BUFF)
        txt_lcd = Text("LCD1602 用于显示相关信息").scale(0.6).next_to(rect_lcd, UP, 1.5)

        self.play(AnimationGroup(ShowCreation(rect_buzzer), Write(txt_buzzer), lag_ratio = 0.5))
        self.play(AnimationGroup(ShowCreation(rect_lcd), Write(txt_lcd), lag_ratio = 0.5))
        self.wait(0.8)
        self.play(*map(FadeOut, (rect_buzzer, rect_lcd, txt_buzzer, txt_lcd)))

class Scene2(Scene):
    def construct(self):
        txt1 = Text("蜂鸣器发声原理：", color = BLUE_B).scale(0.9)
        txt2 = Text("每个音调都有对应的频率").scale(0.7)
        txt3 = VGroup(Text("并且前后音调存在"), Tex("2^{1/12}"), Text("的倍数关系"))\
            .arrange(buff = SMALL_BUFF).scale(0.7)
        txt4 = Text("因此可以控制蜂鸣器振动频率以发出对应的音调").scale(0.7)
        vg = VGroup(txt1, txt2, txt3, txt4).arrange(DOWN, aligned_edge = LEFT).to_corner(UL, buff = LARGE_BUFF)
        srd = SurroundingRectangle(vg, buff = MED_LARGE_BUFF).set_stroke(opacity = 0).set_fill(BLACK, 0.5)

        self.play(FadeIn(srd))
        self.play(DrawBorderThenFill(txt1))
        self.play(Write(txt2))
        self.wait(0.5)
        self.play(Write(txt3))
        self.wait(0.5)
        self.play(Write(txt4))
        self.wait(0.5)
        self.play(*map(FadeOut, (vg, srd)))

class Scene3(Scene):
    def construct(self):
        txt1 = Text("谱子来源于网上的midi版").scale(0.7)
        txt2 = Text("做了一些修改以适配蜂鸣器").scale(0.7)
        txt3 = Text("由于单片机定时不够准确").scale(0.7)
        txt4 = Text("因此有后期调整播放速度来对齐音频").scale(0.7)
        txt5 = Text("可能仍有部分有些许差错").scale(0.7)
        vg = VGroup(
            VGroup(txt1, txt2).arrange(DOWN, aligned_edge = LEFT),
            VGroup(txt3, txt4, txt5).arrange(DOWN, aligned_edge = LEFT)
            ).arrange(DOWN, aligned_edge = LEFT, buff = MED_LARGE_BUFF).to_corner(UL, buff = LARGE_BUFF)
        srd = SurroundingRectangle(vg, buff = MED_LARGE_BUFF).set_stroke(opacity = 0).set_fill(BLACK, 0.5)

        self.play(FadeIn(srd))
        self.play(Write(txt1))
        self.wait(0.5)
        self.play(Write(txt2))
        self.wait(0.8)
        self.play(Write(txt3))
        self.wait(0.5)
        self.play(Write(txt4))
        self.wait(0.5)
        self.play(Write(txt5))
        self.wait(1)
        self.play(*map(FadeOut, (vg, srd)))
        
class Scene4(Scene):
    def construct(self):
        # img = ImageMobject(frame2_path)
        # img.scale(FRAME_WIDTH / img.get_width())
        # self.add(img)
        # img.add_mouse_press_listner(lambda mobj, pos: print(mobj, pos))

        rect_mled = CDRect(np.array([0.75, 2.77, 0]), np.array([2.75, 0.72, 0]))
        rect_mled.set_stroke(YELLOW, 4).set_fill(opacity = 0)
        txt_mled = Text("点阵").scale(0.6).next_to(rect_mled, DOWN, 2.3)
        self.play(AnimationGroup(ShowCreation(rect_mled), Write(txt_mled), lag_ratio = 0.5))
        self.wait(0.8)
        self.play(*map(FadeOut, (rect_mled, txt_mled)))

class Scene5(Scene):
    def construct(self):
        txt1 = Text("点阵显示原理：", color = BLUE_B).scale(0.9)
        txt2 = Text("点阵每次只能显示某一行或者某一列").scale(0.7)
        txt3 = Text("我采用了逐列扫描的方式").scale(0.7)
        txt4 = Text("也就是以高速度的扫描使得从整体上来看都能显示").scale(0.7)
        vg = VGroup(txt1, txt2, txt3, txt4).arrange(DOWN, aligned_edge = LEFT).to_corner(UL, LARGE_BUFF)
        srd = SurroundingRectangle(vg, buff = MED_LARGE_BUFF).set_stroke(opacity = 0).set_fill(BLACK, 0.5)

        self.play(FadeIn(srd))
        self.play(DrawBorderThenFill(txt1))
        self.play(Write(txt2))
        self.wait(0.5)
        self.play(Write(txt3))
        self.wait(0.5)
        self.play(Write(txt4))

        class CCircle(Circle):
            def __init__(self, orgColor, **kwargs):
                super().__init__(**kwargs)
                self.set_stroke(WHITE, 1.5)
                self.set_fill(color = orgColor)
                self.scale(0.15)
        
        vgC = VGroup(
            VGroup(CCircle(WHITE), CCircle(RED), CCircle(RED), CCircle(WHITE)).arrange(DOWN, buff = 0.05),
            VGroup(CCircle(RED), CCircle(WHITE), CCircle(WHITE), CCircle(RED)).arrange(DOWN, buff = 0.05),
            VGroup(CCircle(RED), CCircle(WHITE), CCircle(WHITE), CCircle(RED)).arrange(DOWN, buff = 0.05),
            VGroup(CCircle(WHITE), CCircle(RED), CCircle(RED), CCircle(WHITE)).arrange(DOWN, buff = 0.05)
            ).arrange(RIGHT, buff = SMALL_BUFF).next_to(srd, DOWN, MED_LARGE_BUFF, LEFT).align_to(vg, LEFT)
        tip = ArrowTip(angle = -PI / 2).set_color(YELLOW).scale(0.6)
        def tip_to(ind, cl = True):
            tip.next_to(vgC[ind], UP, buff = SMALL_BUFF)
            if cl:
                curInd = 3 if ind == 0 else ind - 1
                for c in vgC[curInd]:
                    c.set_fill(opacity = 0)
            for c in vgC[ind]:
                c.set_fill(opacity = 1)
        tip_to(0)
        self.play(ShowCreation(tip), FadeIn(vgC))
        for i in range(4):
            self.wait(0.3)
            tip_to(i)
        for i in range(4):
            self.wait(0.1)
            tip_to(i)
        for i in range(4):
            self.wait(0.02)
            tip_to(i)
        for i in range(4):
            self.update_frame()
            self.emit_frame()
            tip_to(i)
        for _ in range(20):
            for i in range(4):
                self.update_frame()
                self.emit_frame()
                tip_to(i, False)
        for i in range(4):
            self.update_frame()
            self.emit_frame()
            tip_to(i)
        for i in range(4):
            self.wait(0.02)
            tip_to(i)
        for i in range(4):
            self.wait(0.1)
            tip_to(i)
        self.wait(0.3)
        tip_to(0)

        self.wait(0.5)
        self.play(FadeOut(vgC), Uncreate(tip))
        self.play(*map(FadeOut, (vg, srd)))

class Scene6(Scene):
    def construct(self):
        txt1 = Text("对于图像数据：", color = BLUE_B).scale(0.9)
        txt2 = Text("我先用ffmpeg将原视频每秒10个拆成一组图片").scale(0.7)
        txt3 = Text("再用Qt库写了一个转换图像的程序").scale(0.7)
        txt4 = Text("其中包含等比缩放到8x8和判断灰度等").scale(0.7)
        vg = VGroup(txt1, txt2, txt3, txt4).arrange(DOWN, aligned_edge = LEFT).to_corner(UL, buff = LARGE_BUFF)
        srd = SurroundingRectangle(vg, buff = MED_LARGE_BUFF).set_stroke(opacity = 0).set_fill(BLACK, 0.5)

        self.play(FadeIn(srd))
        self.play(DrawBorderThenFill(txt1))
        self.play(Write(txt2))
        self.wait(0.5)
        self.play(Write(txt3))
        self.wait(0.5)
        self.play(Write(txt4))
        self.wait(1)
        self.play(*map(FadeOut, (vg, srd)))

class Scene7(Scene):
    def construct(self):
        txt1 = Text("不过由于单片机容量有限").scale(0.7)
        txt2 = Text("因此我将其拆成了4段").scale(0.7)
        vg = VGroup(txt1, txt2).arrange(DOWN, aligned_edge = LEFT).to_corner(UL, buff = LARGE_BUFF)
        srd = SurroundingRectangle(vg, buff = MED_LARGE_BUFF).set_stroke(opacity = 0).set_fill(BLACK, 0.5)

        self.play(FadeIn(srd))
        self.play(Write(txt1))
        self.wait(0.5)
        self.play(Write(txt2))
        self.wait()
        self.play(*map(FadeOut, (vg, srd)))
        

