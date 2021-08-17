import sys
sys.path.append(".")
import header as h
from manimlib import *

txtColor = "#333333"
txtColor2 = "#555555"
digitAvgColor = average_color(BLUE, PINK)
t2c = {
    "New": PURPLE, "GML": GREEN, "Rooms": GREY_BROWN,
    "sprXXX": YELLOW_E, "sXXX" : YELLOW_E, "objXXX": BLUE_D, "oXXX": BLUE_D,
    "Sprite": YELLOW_E, "Object": BLUE_D, "Room": GREY_BROWN, "Script": GREEN_D, "Event": GREEN_D,
    "x": TEAL_D, "y": TEAL_D, "4": digitAvgColor,
    "\"": GOLD
}

class GMOpeningScene(h.OpeningScene):
    str1 = "GameMaker 教程"
    str2 = "入门"

class GMTimeScene(h.TimeScene):
    info_list = [
        ["00:12", "创建项目"],
        ["00:42", "第一次尝试"],
        ["02:16", "完善"],
        ["05:02", "结尾"]
    ]

class CreateProject(Scene):
    def construct(self):
        self.add(h.watermark())
        h.chapter_animate(self, "Ⅰ", "创建项目")

        indHelper = Rectangle()
        def ind(x, y, w, h):
            indHelper.set_width(w, stretch = True).set_height(h, stretch = True).move_to([x, y, 0])
            self.play(ShowCreationThenFadeAround(indHelper))

        txtCP1 = Text("打开GMS2，点击New（新建）即可创建项目", color = txtColor, t2c = t2c).to_edge(UL)
        imgCP1 = ImageMobject("assets/gm/OS.png", height = 4).next_to(txtCP1, DOWN, aligned_edge = LEFT)
        self.play(Write(txtCP1), FadeIn(imgCP1))

        ind(-5.43, 1.775, 1.9, 1.2)
        self.play(FadeOut(imgCP1), run_time = 0.5)

        txtCP2 = Text("接着，如上集所说，这里我们选择GML", color = txtColor, t2c = t2c).next_to(txtCP1, DOWN, aligned_edge = LEFT)
        imgCP2 = ImageMobject("assets/gm/select.png", height = 2).next_to(txtCP2, DOWN, aligned_edge = LEFT)
        self.play(Write(txtCP2), FadeIn(imgCP2))

        ind(-3.25, 1.18, 1.9, 1.2)
        self.play(FadeOut(imgCP2), run_time = 0.5)
        self.play(Uncreate(txtCP1), Uncreate(txtCP2))

        txtL1 = Text("进入项目后，可以看到界面右侧有一个列表", color = txtColor).to_edge(UL)
        imgL1 = ImageMobject("assets/gm/right_list.png", height = 7).to_edge(UR)
        imgL1.set_width(imgL1.get_width() * 0.92, stretch = True)
        self.play(DrawBorderThenFill(txtL1), FadeIn(imgL1))
        self.wait(0.5)

        txtL2 = Text("其中只有Rooms文件夹有内容，这个我们稍后再说", color = txtColor, t2c = t2c)\
            .next_to(txtL1, DOWN, aligned_edge = LEFT)
        g_txtL2 = Text("*GM8没有任何内容", color = txtColor2).scale(0.6).next_to(txtL2, DOWN, SMALL_BUFF, LEFT)
        self.play(Write(txtL2))
        self.play(DrawBorderThenFill(g_txtL2), run_time = 0.5)

        ind(4.77, -1.25, 3.2, 0.2)
        self.play(FadeOut(imgL1), run_time = 0.5)
        
        txtL3 = Text("在列表中 右键-Create（创建）可以添加", color = txtColor, t2c = h.dictAppend({ "右键-Create": PURPLE }, t2c))\
            .next_to(g_txtL2, DOWN, MED_LARGE_BUFF, LEFT)
        imgL3 = ImageMobject("assets/gm/rmouse_menu.png").to_edge(UR)
        txtL4 = Text("Sprite、Object、Room、Script等内容", color = txtColor, t2c = t2c)\
            .next_to(txtL3, DOWN, aligned_edge = LEFT)
        self.play(Write(txtL3), FadeIn(imgL3))
        self.play(Write(txtL4))
        self.wait()

        txtL5 = Text("我将会分别进行介绍", color = txtColor).next_to(txtL4, DOWN, aligned_edge = LEFT)
        self.play(DrawBorderThenFill(txtL5))
        self.wait()

        self.play(*[FadeOut(mobj) for mobj in [txtL1, txtL2, g_txtL2, txtL3, txtL4, txtL5, imgL3]])

class FirstStep_1(Scene):
    def construct(self):
        self.add(h.watermark())
        h.chapter_animate(self, "Ⅱ", "第一步尝试")
        
        txtSprAndObj = Text("首先，你需要知道Sprite和Object", color = txtColor, t2c = t2c)
        self.play(DrawBorderThenFill(txtSprAndObj))
        self.wait(0.5)
        self.play(FadeOut(txtSprAndObj))

        txtSpr = Text("什么是Sprite?", color = txtColor, t2c = t2c).to_edge(UL)
        self.play(DrawBorderThenFill(txtSpr))
        self.wait(0.5)

        txtSpr1 = VGroup(
            Text("-", color = txtColor2), 
            Text("Sprite是一个图像（序列），你可以对其进行编辑或者导入现有的图像", color = txtColor2, t2c = h.dictAppend({ "（序列）": GREY_B }, t2c))
            ).arrange().scale(0.8).next_to(txtSpr, DOWN, aligned_edge = LEFT)
        self.play(FadeIn(txtSpr1, scale_factor = 0.7))
        self.wait(0.8)
        
        txtSpr2 = VGroup(
            Text("-", color = txtColor2),
            Text("创建一个Sprite后，你便可以在需要的地方使用它", color = txtColor2, t2c = t2c)
            ).arrange().scale(0.8).next_to(txtSpr1, DOWN, aligned_edge = LEFT)
        self.play(FadeIn(txtSpr2, scale_factor = 0.7))
        self.wait()

        txtObj = Text("什么是Object?", color = txtColor, t2c = t2c).next_to(txtSpr2, DOWN, MED_LARGE_BUFF, LEFT)
        self.play(DrawBorderThenFill(txtObj))
        self.wait(0.5)

        txtObj1 = VGroup(
            Text("-", color = txtColor2),
            Text("Object是游戏的重要部分", color = txtColor2, t2c = t2c).insert_n_curves(50)
            ).arrange().scale(0.8).next_to(txtObj, DOWN, aligned_edge = LEFT)
        self.play(FadeIn(txtObj1, scale_factor = 0.7))
        self.wait(0.8)

        txtObj2 = VGroup(Text("-", color = txtColor2), Text("玩家、物品、敌人等都需要它来实现", color = txtColor2))\
            .arrange().scale(0.8).next_to(txtObj1, DOWN, aligned_edge = LEFT)
        self.play(FadeIn(txtObj2, scale_factor = 0.7))
        self.wait()

        txtN1 = Text("有点懵?", color = txtColor)
        txtN2 = Text("让我们通过实践来加深印象", color = txtColor2).insert_n_curves(500).scale(0.8)
        groupN = VGroup(txtN1, txtN2).arrange().next_to(txtObj2, DOWN, LARGE_BUFF, LEFT)
        self.play(DrawBorderThenFill(txtN1))
        self.wait(0.5)
        self.play(Write(txtN2))
        self.wait()

        self.play(*[FadeOut(mobj) for mobj in [txtSpr, txtSpr1, txtSpr2, txtObj, txtObj1, txtObj2, groupN]])

class FirstStep_2(Scene):
    def construct(self):
        self.add(h.watermark())

        indHelper = Rectangle()
        def indAnimate(x, y, w, h):
            indHelper.set_width(w, stretch = True).set_height(h, stretch = True).move_to([x, y, 0])
            return ShowCreationThenFadeAround(indHelper)

        txtE1 = Text("首先，分别创建一个Sprite和Object", color = txtColor, t2c = t2c)\
            .to_edge(UL)
        imgE1_2 = ImageMobject("assets/gm/new_object.png", height = 0.7).to_edge(UR)
        imgE1_1 = ImageMobject("assets/gm/new_sprite.png", height = 0.7).next_to(imgE1_2, LEFT)
        txtE1_note1 = Text("建议将Sprite命名为sprXXX或sXXX", color = txtColor2, t2c = t2c)\
            .scale(0.5).next_to(imgE1_1, LEFT, aligned_edge = UP)
        txtE1_note2 = Text("将Object命名为objXXX或oXXX", color = txtColor2, t2c = t2c)\
            .scale(0.5).next_to(txtE1_note1, DOWN, SMALL_BUFF, RIGHT)
        self.play(
            DrawBorderThenFill(txtE1), FadeIn(imgE1_1), FadeIn(imgE1_2),
            DrawBorderThenFill(txtE1_note1), DrawBorderThenFill(txtE1_note2)
            )
        self.wait()

        txtE2 = Text("双击打开Sprite的编辑界面", color = txtColor2, t2c = t2c)\
            .scale(0.8).next_to(txtE1, DOWN, aligned_edge = LEFT)
        imgE2 = ImageMobject("assets/gm/edit_sprite.png", height = 5)
        imgE2.move_to([0, txtE2.get_bottom()[1] - DEFAULT_MOBJECT_TO_MOBJECT_BUFFER - imgE2.get_height() / 2, 0])
        self.play(Write(txtE2), FadeIn(imgE2, scale_factor = 1.3), run_time = 1)

        txtE2_1 = Text("调整大小").scale(0.7).move_to([-3.8, 0.9, 0])
        txtE2_2 = Text("编辑图像").scale(0.7)
        txtE2_2.move_to([-2.1 + txtE2_2.get_width() / 2, 1.4, 0])
        txtE2_3 = Text("导入现有图像").scale(0.7)
        txtE2_3.move_to([-2.1 + txtE2_3.get_width() / 2, 1.12, 0])
        self.add(txtE2_1)
        self.play(
            indAnimate(-4.055, 1.22, 0.2, 0.2), indAnimate(-2.65, 1.4, 0.76, 0.1), indAnimate(-2.65, 1.12, 0.76, 0.1),
            *[DrawBorderThenFill(mobj) for mobj in [txtE2_1, txtE2_2, txtE2_3]]
            )
        self.wait()

        txtE3 = Text("比如可以随便糊几笔....", color = txtColor).scale(0.8).next_to(imgE2, DOWN)
        self.play(Write(txtE3))
        self.wait(0.8) # n8

        # -> 后期插入视频 <- #

        self.remove(imgE2, txtE2_1, txtE2_2, txtE2_3, txtE3)
        self.wait(0.5)

        txtE4 = Text("打开Object的编辑界面", color = txtColor2, t2c = t2c)\
            .scale(0.8).next_to(txtE1, DOWN, aligned_edge = LEFT)
        imgE4 = ImageMobject("assets/gm/edit_object.png", height = 5)
        self.play(ReplacementTransform(txtE2, txtE4), FadeIn(imgE4, scale_factor = 1.3))
        self.wait(0.5)

        txtE5 = Text("就可以将弄好的Sprite设置到Object上", color = txtColor, t2c = t2c)\
            .scale(0.8).next_to(imgE4, DOWN).insert_n_curves(50)
        self.play(Write(txtE5))
        self.play(indAnimate(-1.33, 0.78, 1.5, 0.2))
        self.wait(0.5)

        txtE6 = Text("也就是说，设置了这个Object在游戏中的样子", color = txtColor2, t2c = t2c).scale(0.7).next_to(txtE5, DOWN, SMALL_BUFF)
        imgE6 = ImageMobject("assets/gm/edit_object_done.png", height = 5).move_to(imgE4)
        self.play(DrawBorderThenFill(txtE6), FadeIn(imgE6))
        self.remove(imgE4)
        self.wait(2)

        self.play(*[FadeOut(mobj) for mobj in [txtE1, imgE1_1, imgE1_2, txtE1_note1, txtE1_note2, txtE4, txtE5, txtE6, imgE6]])

class FirstStep_3(Scene):
    def construct(self):
        self.add(h.watermark())

        indHelper = Rectangle()
        def indAnimate(x, y, w, h):
            indHelper.set_width(w, stretch = True).set_height(h, stretch = True).move_to([x, y, 0])
            return ShowCreationThenFadeAround(indHelper)

        txt1 = Text("现在", color = txtColor)
        txt2 = Text("，我们有一个设置好Sprite的Object", color = txtColor, t2c = t2c).insert_n_curves(50)
        group = VGroup(txt1, txt2).arrange(buff = SMALL_BUFF)
        self.play(Write(txt1), run_time = 0.5)
        self.wait(0.5)
        self.play(Write(txt2))
        self.wait(0.5)
        self.play(group.animate.to_edge(UL))
        
        txt3 = Text("让我们回到这个一开始自带的Room", color = txtColor, t2c = t2c).scale(0.8).next_to(txt1, DOWN, MED_LARGE_BUFF, LEFT)
        img3 = ImageMobject("assets/gm/new_room.png", height = 1).next_to(txt3, DOWN, aligned_edge = LEFT)
        self.play(Write(txt3), FadeIn(img3))

        txt3_note = Text("*GM8需自行创建", color = txtColor2).scale(0.6).next_to(txt3, aligned_edge = DOWN)
        self.play(DrawBorderThenFill(txt3_note), run_time = 0.5)
        self.wait(0.8)

        txt4 = Text(
            "如果说Object是游戏中的角色，那么Room就是角色表演的舞台", color = txtColor, 
            t2c = h.dictAppend({ "角色": BLUE_D, "舞台": GREY_BROWN }, t2c)
            ).scale(0.8).next_to(img3, DOWN, aligned_edge = LEFT)
        self.play(Write(txt4), run_time = 3)
        self.wait()

        txt5 = Text("接着，我们打开Room的编辑界面，将Object拖入Room中", color = txtColor, t2c = t2c)\
            .scale(0.8).next_to(txt4, DOWN, aligned_edge = LEFT)
        self.play(Write(txt5))
        self.wait()

        # -> 后期插入视频 <- #

        self.remove(group, txt3, img3, txt3_note, txt4, txt5)

        self.wait(0.5)
        imgToolBar = ImageMobject("assets/gm/tool_bar.png", height = 1).to_edge(UL, MED_LARGE_BUFF)
        txt6 = Text("接着，点击工具栏的运行按钮即可查看效果", color = txtColor, t2c = h.dictAppend({"运行": PURPLE}, t2c))\
            .scale(0.8).next_to(imgToolBar, DOWN, aligned_edge = LEFT)
        self.play(FadeIn(imgToolBar), DrawBorderThenFill(txt6))
        self.play(indAnimate(-3.57, 2.95, 0.2, 0.2))

        imgResult = ImageMobject("assets/gm/first_step_result.png", height = 5)
        self.play(
            imgToolBar.animate.set_opacity(0.3), txt6.animate.set_opacity(0.3), 
            FadeIn(imgResult, scale_factor = 1.3)
            )
        self.wait(0.5)

        txt7 = Text("可以看到，目前只有画面，无法进行操作", color = txtColor2).scale(0.7).next_to(imgResult, DOWN)
        self.play(DrawBorderThenFill(txt7))
        self.wait(2)
        
        self.play(*[FadeOut(mobj) for mobj in [imgToolBar, txt6, imgResult, txt7]])
        
class Better_1(Scene):
    def construct(self):
        self.add(h.watermark())
        h.chapter_animate(self, "Ⅲ", "完善")

        indHelper = Rectangle()
        def indAnimate(x, y, w, h):
            indHelper.set_width(w, stretch = True).set_height(h, stretch = True).move_to([x, y, 0])
            return ShowCreationThenFadeAround(indHelper)

        txtN1 = Text("目前的效果不能操作", color = txtColor).shift(UP * 0.5)
        self.play(DrawBorderThenFill(txtN1))
        txtN2 = Text("所以我们需要继续添加功能", color = txtColor2).next_to(txtN1, DOWN)
        self.play(Write(txtN2))
        self.wait(0.8)
        self.play(FadeOut(txtN1), FadeOut(txtN2))

        txtObj = Text("回到Object的编辑界面", color = txtColor, t2c = t2c).to_edge(UL)
        imgObj = ImageMobject("assets/gm/edit_object_done.png", height = 4).to_edge(UR)
        self.play(DrawBorderThenFill(txtObj), FadeIn(imgObj))
        self.wait(0.5)

        txtEv1 = Text("可以看到，这里有个Events（事件）界面", color = txtColor2, t2c = t2c)\
            .scale(0.8).next_to(txtObj, DOWN, aligned_edge = LEFT)
        self.play(Write(txtEv1))
        self.wait(0.3)

        txtEv2 = Text("添加Event便可以让Object运作起来", color = txtColor2, t2c = t2c)\
            .scale(0.8).next_to(txtEv1, DOWN, aligned_edge = LEFT)
        self.play(Write(txtEv2))
        self.play(indAnimate(5.38, 1.06, 2.15, 0.15)) # n13
        self.wait(0.8)

        
        txtEv3 = Text("选择KeyDown（压住键）中的Right（右方向键）", color = txtColor2, t2c = { "KeyDown": PURPLE, "Right": PURPLE })\
            .scale(0.8).next_to(txtEv2, DOWN, MED_LARGE_BUFF, LEFT)
        txtEv4 = Text("即可添加一个当按着右方向键时就会触发的事件", color = txtColor2, t2c = { "按着右方向键": PURPLE, "事件": GREEN_D })\
            .scale(0.8).next_to(txtEv3, DOWN, aligned_edge = LEFT)
        imgEv = ImageMobject("assets/gm/add_key_event.png", height = 5).to_edge(UR)
        self.play(Write(txtEv3), FadeTransform(imgObj, imgEv), run_time = 2)
        self.play(Write(txtEv4), run_time = 2)
        self.play(indAnimate(5.03, 1.7, 1, 0.13), indAnimate(6.05, 1.51, 0.8, 0.08))
        self.wait(0.8)

        self.play(*[Uncreate(mobj) for mobj in [txtObj, txtEv1, txtEv2, txtEv3, txtEv4]], FadeOut(imgEv), run_time = 1)

class Better_2(Scene):
    def construct(self):
        self.add(h.watermark())

        indHelper = Rectangle()
        def indAnimate(x, y, w, h):
            indHelper.set_width(w, stretch = True).set_height(h, stretch = True).move_to([x, y, 0])
            return ShowCreationThenFadeAround(indHelper)

        txtEdit1 = Text("进入事件的编辑界面", color = txtColor2, t2c = { "事件": GREEN_D }).scale(0.8).to_edge(UL)
        self.play(Write(txtEdit1))

        codeRight = h.CodeView(
            "Key Down - Right", 
            [
                "/// @description Insert description here",
                "// You can write your code in this editor",
                "x = x + 4;"
            ], 
            t2c, headerColor = GREEN_D
            ).next_to(txtEdit1, DOWN, aligned_edge = LEFT)
        codeRight.lines[0].set_color(GREEN_D)
        codeRight.lines[1].set_color(GREEN_D)
        self.play(FadeIn(Group(codeRight.others, codeRight.lines[0], codeRight.lines[1]), UP))

        g_txt1 = Text("*在GM8中，需要拖动一个代码功能块才能编辑代码", color = txtColor2).scale(0.6).to_edge(UR)
        g_img1 = ImageMobject("assets/gm/gm8_add_code.png", height = 4.5).next_to(g_txt1, DOWN, aligned_edge = RIGHT)
        g_img2 = ImageMobject("assets/gm/gm8_code.png", height = 3).next_to(g_txt1, DOWN, aligned_edge = RIGHT)
        g_arrow = Arrow([5.65, 1.12, 0], [4.3, 2.5, 0], fill_color = BLUE_D, buff = 0)
        self.play(DrawBorderThenFill(g_txt1), FadeIn(g_img1))
        self.play(GrowArrow(g_arrow), indAnimate(6.5, 1.35, 0.1, 0.43), indAnimate(5.65, 1.12, 0.2, 0.2))
        self.play(FadeOut(g_arrow))
        self.wait()
        self.play(FadeTransform(g_img1, g_img2))
        self.wait(0.5)
        self.play(FadeOut(g_txt1), FadeOut(g_img2)) # n9

        txtEdit2 = Text("比如，我想要让它这个时候“向右移动4个像素”", color = txtColor2, t2c = { "[13:21]": PURPLE })\
            .scale(0.8).next_to(codeRight, DOWN, aligned_edge = LEFT)
        self.play(Write(txtEdit2))
        self.wait(0.8)

        self.play(Group(txtEdit1, codeRight.others, codeRight.lines[0], codeRight.lines[1], txtEdit2).animate.set_opacity(0.2))
        txtAxe = Text("首先我们要知道GM的坐标系统", color = txtColor, t2c = { "坐标系统": PURPLE })
        axeUnderlineY = FRAME_Y_RADIUS - (DEFAULT_MOBJECT_TO_EDGE_BUFFER + 0.1 + txtAxe.get_height() + 0.16)
        axeUnderline = Line([-1.8, axeUnderlineY, 0], [1.8, axeUnderlineY, 0], color = txtColor)
        self.play(DrawBorderThenFill(txtAxe))
        self.wait(0.5) # n13
        self.play(txtAxe.animate.to_corner(UP, buff = DEFAULT_MOBJECT_TO_EDGE_BUFFER + 0.1), GrowArrow(axeUnderline))
        
        txtAxe1 = Text("在GM中，左上角为Room原点，向右向下为正方向", color = txtColor, t2c = t2c)\
            .scale(0.8).to_corner(DOWN)
        self.play(Write(txtAxe1))

        gmnp = h.GMRoomPlane(4.5, 4.5, txtColor)
        self.play(gmnp.animate1(), run_time = 1.5)
        self.play(*gmnp.animate2Array())
        self.wait(0.8)

        txtAxe2 = Text("x和y确定了物件在Room中的位置", color = txtColor, t2c = t2c)\
            .scale(0.8).move_to(txtAxe1)
        self.play(ReplacementTransform(txtAxe1, txtAxe2), run_time = 1.8)

        gmdot = Dot(color = TEAL)
        gmpos = Text("(x, y)", color = txtColor, t2c = t2c)\
            .scale(0.7).next_to(gmdot, UR, 0)
        always(gmpos.next_to, gmdot, UR, 0)
        self.play(Write(gmdot), Write(gmpos))
        self.wait(0.5) # n20

        gmdot_center = gmdot.get_center()
        path1 = bezier([gmdot_center, gmdot_center + (LEFT * 0.4 + UP * 0.9) * 1.5, gmdot_center + (LEFT + UP * 0.7) * 1.5])
        path2 = bezier([gmdot_center + (LEFT + UP * 0.7) * 1.5, gmdot_center + (LEFT * 0.6 + DOWN * 0.2) * 1.5, gmdot_center])
        pathAnimate1 = MoveAlongPath(gmdot, VMobject().add_subpath([path1(t / 50) for t in range(0, 51)]))
        pathAnimate2 = MoveAlongPath(gmdot, VMobject().add_subpath([path2(t / 50) for t in range(0, 51)]))
        self.play(pathAnimate1, run_time = 1.5)
        self.wait(0.5)
        self.play(pathAnimate2, run_time = 1.5)

        gmspr = ImageMobject("assets/gm/sprite.png", height = 1)
        f_always(gmspr.move_to, lambda: gmdot.get_center() + [gmspr.get_width() / 2, -gmspr.get_height() / 2, 0])
        self.remove(gmdot)
        self.add(gmspr, gmdot)
        self.play(FadeIn(gmspr))
        self.play(pathAnimate1, run_time = 1.5)
        self.wait(0.5)
        self.play(pathAnimate2, run_time = 1.5)
        self.wait(0.5) # n28

        self.play(FadeOut(gmspr), run_time = 0.5)
        self.play(
            FadeOut(Group(txtAxe, axeUnderline, gmnp, txtAxe2, gmdot, gmpos)),
            Group(txtEdit1, txtEdit2, codeRight.others, codeRight.lines[0], codeRight.lines[1]).animate.set_opacity(1)
            )

        txtEdit3 = VGroup(
            Text("那我们就可以写上", color = txtColor2),
            Text("\"x = x + 4;\"", color = txtColor2, t2c = t2c)
            ).set_stroke(txtColor2).arrange(buff = SMALL_BUFF).scale(0.8)
        txtEdit4 = Text("我们不能从数学的角度来思考这段代码", color = txtColor2, t2c = { "数学": ORANGE }).scale(0.8)
        txtEdit5 = Text("从编程的角度，这段代码的意思是：“将x的值设置为x+4的结果”", color = txtColor2, t2c = h.dictAppend({ "编程": ORANGE }, t2c)).scale(0.8)
        txtEdit6 = Text("这样就可以使得x增加4", color = txtColor2, t2c = t2c).scale(0.8)
        group3to6 = Group(txtEdit3, txtEdit4, txtEdit5, txtEdit6).arrange(DOWN, aligned_edge = LEFT).next_to(txtEdit2, DOWN, aligned_edge = LEFT)
        self.play(Write(txtEdit3))
        self.play(Write(codeRight.lines[2]))
        self.wait()
        self.play(Write(txtEdit4))
        self.wait(0.5)
        self.play(Write(txtEdit5), run_time = 3)
        self.wait(1.5)
        self.play(Write(txtEdit6))
        self.wait(2.5) # n39

        self.play(Uncreate(Group(txtEdit2, group3to6)), run_time = 1.5)

        txtEdit7 = VGroup(
            Text("这段代码同样可以写成", color = txtColor2),
            Text("\"x += 4;\"", color = txtColor2, t2c = t2c)
            ).set_stroke(txtColor2).arrange(buff = SMALL_BUFF).scale(0.8)
        txtEdit8 = VGroup(
            Text("这是一种简略写法，和", color = txtColor2, t2c = { "简略写法": ORANGE }),
            Text("\"x = x + 4;\"", color = txtColor2, t2c = t2c),
            Text("的效果是一样的", color = txtColor2)
            ).set_stroke(txtColor2).arrange(buff = SMALL_BUFF).scale(0.8)
        txtEdit9 = Text("结尾的分号表示这一部分结束", color = txtColor2, t2c = { "分号": PURPLE }).scale(0.8)
        txtEdit10 = Text("GM允许你省略结尾的分号，但是我建议加上", color = txtColor2, t2c = { "分号": PURPLE }).scale(0.8)
        group7to10 = Group(txtEdit7, txtEdit8, txtEdit9, txtEdit10).arrange(DOWN, aligned_edge = LEFT).next_to(codeRight, DOWN, aligned_edge = LEFT)
        self.play(Write(txtEdit7))
        codeRight.lines.replaceAnimate(lambda a: self.play(a), 2, "x += 4;", t2c = t2c)
        self.wait(0.5)
        self.play(Write(txtEdit8))
        self.wait(1.5)
        self.play(Write(txtEdit9))
        self.wait(0.5)
        self.play(Write(txtEdit10))
        self.wait(1.5) # n49

        txtWarn1 = Text(
            "注意：在初次编程时很容易将英文符号写成中文符号（如结尾的分号）", 
            color = txtColor2, t2c = { "注意": RED_D, "分号": PURPLE }
            ).scale(0.8)
        txtWarn2 = Text("请在输入这些符号时关闭输入法", color = txtColor2).scale(0.8)
        groupWarn = Group(txtWarn1, txtWarn2).arrange(DOWN, aligned_edge = LEFT).next_to(txtEdit10, DOWN, MED_LARGE_BUFF, LEFT)
        txtWarn2.shift(RIGHT * 0.5)
        self.play(Write(txtWarn1), run_time = 2.5)
        self.play(Write(txtWarn2), run_time = 1.3)
        self.wait(2) # n53

        self.play(FadeOut(Group(txtEdit1, group7to10, groupWarn)))
        
class Better_3(Scene):
    def construct(self):
        self.add(h.watermark())

        indHelper = Rectangle()
        def indAnimate(x, y, w, h):
            indHelper.set_width(w, stretch = True).set_height(h, stretch = True).move_to([x, y, 0])
            return ShowCreationThenFadeAround(indHelper)

        codeRight = h.CodeView(
            "Key Down - Right",
            [
                "/// @description Insert description here",
                "// You can write your code in this editor",
                "x += 4;"
            ],
            t2c, headerColor = GREEN_D
            ).move_to([-3.944761, 2.24487825, 0])
        codeRight.lines[0].set_color(GREEN_D)
        codeRight.lines[1].set_color(GREEN_D)
        self.add(codeRight)
        self.play(codeRight.animate.to_edge(UL), run_time = 0.7)

        txtDesc1 = VGroup(
            Text("你可能有注意到代码编辑界面上的", color = txtColor2),
            Text("\"/// @description ...\"", color = GREEN_D, t2c = t2c)
            ).set_stroke(txtColor2).arrange(buff = SMALL_BUFF).scale(0.8)
        txtDesc2 = Text("这是用来给事件作备注用的", color = txtColor2, t2c = { "事件": GREEN_D, "备注": GREEN_D }).scale(0.8)
        g_txtDesc = Text("*GM8没有该功能", color = txtColor2).scale(0.6)
        txtDesc3 = VGroup(
            Text("比如写上", color = txtColor2),
            Text("\"/// @description 向右移动", color = txtColor2, t2c = h.dictAppend({ "[1:22]": GREEN_D }, t2c)),
            Text("\"", color = GOLD, font = "Noto Sans Light"),
            Text("，就可以在Events中看到备注", color = txtColor2, t2c = t2c)
            ).set_stroke(txtColor2).arrange(aligned_edge = UP, buff = SMALL_BUFF).scale(0.8)
        imgDesc3 = ImageMobject("assets/gm/event_description.png", height = 1.5)
        txtDesc4 = Text("第二行只是一个小提示，删掉也不会有影响", color = txtColor2).scale(0.8)
        groupDesc1to4 = Group(txtDesc1, Group(txtDesc2, g_txtDesc).arrange(), txtDesc3, txtDesc4)\
            .arrange(DOWN, aligned_edge = LEFT).next_to(codeRight, DOWN, aligned_edge = LEFT)
        imgDesc3.next_to(txtDesc3, DOWN, aligned_edge = LEFT)
        self.play(Write(txtDesc1))
        self.play(ShowCreationThenFadeAround(codeRight.lines[0]))
        self.wait(0.8)
        self.play(Write(txtDesc2))
        self.play(DrawBorderThenFill(g_txtDesc))
        self.wait()
        self.play(Write(txtDesc3), run_time = 3)
        codeRight.lines.replaceAnimate(lambda a: self.play(a), 0, "/// @description 向右移动", color = GREEN_D)
        self.play(FadeIn(imgDesc3))
        self.play(indAnimate(-4.75, -0.3, 0.5, 0.15))
        self.wait()
        self.play(FadeOut(imgDesc3), Write(txtDesc4))
        self.wait()
        self.play(codeRight.lines[1].animate.set_opacity(0.3))
        self.wait(2) # n13

        self.play(FadeOut(groupDesc1to4), FadeOut(codeRight))

class Better_4(Scene):
    def construct(self):
        self.add(h.watermark())

        codeRight = h.CodeView(
            "Key Down - Right",
            [
                "/// @description 向右移动",
                "x += 4;"
            ],
            t2c, headerColor = GREEN_D
            ).to_edge(UR)
        codeRight.lines[0].set_color(GREEN_D)
        self.play(FadeIn(codeRight))
        self.wait(0.5)

        txtL1 = Text("我们再添加一个按着左方向键就会触发的事件", color = txtColor2, t2c = { "按着左方向键": PURPLE, "事件": GREEN_D }).scale(0.8)
        codeLeft = h.CodeView(
            "Key Down - Left",
            [
                "/// @description 向左移动",
                "x -= 4;"
            ],
            t2c = t2c, headerColor = GREEN_D
            )
        codeLeft.lines[0].set_color(GREEN_D)
        txtL2 = VGroup(
            Text("写上", color = txtColor2), Text("\"x -= 4;\"", color = txtColor2, t2c = t2c),
            Text("也就是", color = txtColor2), Text("\"x = x - 4;\"", color = txtColor2, t2c = t2c),
            Text("的简略写法", color = txtColor2)
            ).set_stroke(txtColor2).arrange(buff = SMALL_BUFF).scale(0.8)
        txtL3 = Text("就可以让他这个时候向左移动4个像素", color = txtColor2, t2c = t2c).scale(0.8)
        Group(txtL1, codeLeft, txtL2, txtL3).arrange(DOWN, aligned_edge = LEFT).to_edge(UL)
        self.play(Write(txtL1))
        self.wait(0.5)
        self.play(FadeIn(codeLeft.others, UP))
        self.wait(0.5)
        self.play(Write(txtL2))
        self.play(FadeIn(codeLeft.lines))
        self.wait()
        self.play(Write(txtL3))
        self.wait(2) # n11
        
        codeDown = h.CodeView(
            "Key Down - Down",
            [
                "/// @description 向下移动",
                "y += 4;"
            ],
            t2c, headerColor = GREEN_D
            )
        codeDown.lines[0].set_color(GREEN_D)
        codeUp = h.CodeView(
            "Key Down - Up",
            [
                "/// @description 向上移动",
                "y -= 4;"
            ],
            t2c, headerColor = GREEN_D
            ).next_to(codeDown, UP)
        codeUp.lines[0].set_color(GREEN_D)
        self.play(
            FadeOut(Group(txtL1, txtL2, txtL3)),
            codeLeft.animate.next_to(codeDown, LEFT), codeRight.animate.next_to(codeDown, RIGHT)
            )
        
        txtMove = Text("同理，我们可以完成对y的控制", color = txtColor, t2c = t2c).scale(0.8).next_to(codeDown, DOWN, MED_LARGE_BUFF)
        self.play(DrawBorderThenFill(txtMove))
        self.play(FadeIn(Group(codeDown, codeUp)))
        self.wait(1.5)

        group1 = Group(codeUp, codeDown, codeLeft, codeRight, txtMove)
        self.play(group1.animate.set_opacity(0.15))
        
        txtRun = Text("接着运行游戏，我们便可以用方向键让它移动起来", color = txtColor, t2c = { "方向键": PURPLE }).scale(0.9)
        self.play(DrawBorderThenFill(txtRun))
        self.wait(0.8)

        # ->插入视频<- #

        self.remove(txtRun)

        txtW1 = Text("可能有人会问：“你写的是‘向XX方向移动XXX像素’，为什么它会持续移动?”", color = txtColor2, t2c = { "[13:25]": PURPLE, "持续移动": PURPLE }).scale(0.8)
        txtW2 = Text("因为游戏默认会每秒检测这种事件60次（也就是帧率60）", color = txtColor2, t2c = { "60": digitAvgColor, "帧率": PURPLE }).scale(0.8)
        txtW3 = Text("每次执行被称为“Step（步）”", color = txtColor2, t2c = { "Step": PURPLE }).scale(0.8)
        txtW4 = Text("所以产生了持续移动的效果", color = txtColor2, t2c = { "持续移动": PURPLE }).scale(0.8)
        txtW5 = Text("如果调高移动的像素，那么就会移动地更快", color = txtColor2, t2c = { "高": MAROON, "快": MAROON }).scale(0.8)
        group2 = Group(txtW1, txtW2, txtW3, txtW4, txtW5).arrange(DOWN)
        self.play(DrawBorderThenFill(txtW1))
        self.wait()
        self.play(Write(txtW2))
        self.wait(0.8)
        self.play(Write(txtW3))
        self.wait()
        self.play(Write(txtW4))
        self.wait(0.8)
        self.play(Write(txtW5))
        self.wait(2.5)

        self.play(FadeOut(Group(group1, group2)))

class End(Scene):
    def construct(self):
        self.add(h.watermark())

        txt1 = Text("本集教程主要是让你对GM的运作有个简单的认识", color = txtColor2)
        txt2 = Text("接下来的几集我将会系统性地对GM各个方面的内容进行讲解", color = txtColor2)
        group = Group(txt1, txt2).arrange(DOWN)
        self.play(Write(txt1), run_time = 2.5)
        self.wait(0.6)
        self.play(DrawBorderThenFill(txt2), run_time = 2.7)
        self.wait()
        self.play(FadeOut(group))

class GMEndScene(h.EndScene):
    strBgm = "Icy Summit - Triodust、 Aurora Palace - Triodust、 LAST 100SEC - Triodust"

