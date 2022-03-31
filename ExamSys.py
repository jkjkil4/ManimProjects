from manimlib import *

class FirstScene(Scene):
    def construct(self):
        txt1 = Text("源代码:", slant = ITALIC, color = GREY_D).scale(0.6)
        txt1_1 = Text("教师端: https://gitee.com/jkjkil4/ExamSysTeacher", slant = ITALIC, color = GREY).scale(0.4)
        txt1_2 = Text("考生端: https://gitee.com/jkjkil4/ExamSysStudent", slant = ITALIC, color = GREY).scale(0.4)
        vgTxt1 = VGroup(txt1, txt1_1, txt1_2).arrange(DOWN, aligned_edge = LEFT)
        txt1.shift(LEFT * 0.5)

        txt2 = Text("可执行文件:", slant = ITALIC, color = GREY_D).scale(0.6)
        txt2_1 = Text("教师端: https://gitee.com/jkjkil4/ExamSysTeacher/releases", slant = ITALIC, color = GREY).scale(0.4)
        txt2_2 = Text("考生端: https://gitee.com/jkjkil4/ExamSysStudent/releases", slant = ITALIC, color = GREY).scale(0.4)
        vgTxt2 = VGroup(txt2, txt2_1, txt2_2).arrange(DOWN, aligned_edge = LEFT)
        txt2.shift(LEFT * 0.5)

        vgTxt1_2 = VGroup(vgTxt1, vgTxt2).arrange(DOWN, aligned_edge = LEFT, buff = MED_LARGE_BUFF)
        self.add(vgTxt1_2)
        self.wait(0.9)
        self.play(FadeOut(vgTxt1_2), run_time = 0.1)

class ExampleScene(Scene):
    def construct(self):
        txt1 = Text("效果演示", color = GREY_D).scale(0.9).to_edge(TOP, buff = 0.15)
        self.play(FadeIn(txt1, DOWN))
        self.wait(2)
        self.play(FadeOut(txt1, UP))

class TitleTextScene(Scene):
    txt = "None"
    def construct(self):
        txt1 = Text(self.txt, color = WHITE).scale(0.8).to_edge(TOP, buff = MED_SMALL_BUFF).shift(DR * 0.05)
        txt2 = txt1.copy().set_color(GREY_D).shift(UL * 0.05)
        self.add(txt1, txt2)
        self.wait()

class ClientTitleTextScene(TitleTextScene):
    txt = "考生端"
class ServerTitleTextScene(TitleTextScene):
    txt = "教师端"

class FunctionsScene(Scene):
    def construct(self):
        txt1 = Text("细节演示", color = GREY_D).scale(0.9).to_edge(TOP, buff = 0.15)
        self.play(FadeIn(txt1, DOWN))
        self.wait(2)
        self.play(FadeOut(txt1, UP))

class FunctionsCoverScene(Scene):
    def construct(self):
        self.wait()
        flist = [
            "1. 题目编辑",
            "2. 身份验证",
            "3. 掉线重连",
            "4. 错题定位",
        ]
        txtlist = [Text(f, slant = ITALIC).scale(2.5).set_fill(opacity = 0).set_stroke(GREY, 2, 1) for f in flist]
        def showtxt(txt: Text):
            txt.set_stroke(GREY_A)
            self.add(txt)
            self.wait(0.1)
            self.remove(txt)
            self.wait(0.1)
            txt.set_stroke(GREY)
            self.add(txt)
            self.wait(0.8)
            self.play(FadeOut(txt[0:3]), txt[3:].animate.move_to(ORIGIN).set_stroke(opacity = 0.5).scale(3), run_time = 0.8)
            self.wait(2)
        for txt in txtlist:
            showtxt(txt)
            self.play(FadeOut(txt[3:]), run_time = 0.5)
        self.wait()

class CodeScene(Scene):
    def construct(self):
        txt1 = Text("代码使用Qt(C++类库)编写", color = GREY_D, slant = ITALIC)
        txt2 = Text("教师端代码: 2558 行", color = GREY_D, slant = ITALIC)
        txt3 = Text("考生端代码: 1537 行", color = GREY_D, slant = ITALIC)
        txt4 = Text("使用了静态编译将程序打包为单文件", color = GREY_D, slant = ITALIC).scale(0.55)
        vg1 = VGroup(txt1, txt2, txt3).scale(0.55).arrange(DOWN, aligned_edge = LEFT)
        txt1.shift(LEFT * 0.5)
        vg = VGroup(vg1, txt4).arrange(DOWN, aligned_edge = LEFT, buff = LARGE_BUFF).to_edge(LEFT, 3)
        self.play(AnimationGroup(*map(lambda m: FadeIn(m, LEFT), (txt1, txt2, txt3, txt4)), lag_ratio = 0.1, rate_func = rush_from))
        self.wait()
        self.play(AnimationGroup(*map(lambda m: FadeOut(m, LEFT), (txt1, txt2, txt3, txt4)), lag_ratio = 0.1, rate_func = rush_into))
        self.wait(0.5)

class BriefScene(Scene):
    class Server(VGroup):   # 1 x 0.75
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

    class Client(VGroup):
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

    def construct(self):
        txt1 = Text("简要原理", color = GREY_D).scale(0.9).to_edge(TOP, buff = 0.15)
        self.play(FadeIn(txt1, DOWN))
        clientsrow = VGroup(*[self.Client() for _ in range(0, 3)]).arrange(RIGHT, buff = 1)
        clients = VGroup(clientsrow, *[clientsrow.copy() for _ in range(0, 2)]).arrange(DOWN, buff = 0.4).shift(DOWN)
        clientsall = []
        for row in clients:
            for client in row:
                clientsall.append(client)
        server = self.Server().next_to(clients, UP, 0.8)
        self.play(FadeIn(server, run_time = 1), AnimationGroup(*map(lambda m: FadeIn(m), clientsall), lag_ratio = 0.1))

        txtClient = Text("考生端").set_fill(GREY, 0.5).set_stroke(GREY, 1, 1).scale(0.7).move_to(clients).shift(DOWN * 0.55)
        txtServer = Text("教师端").set_fill(GREY, 0.5).set_stroke(GREY, 1, 1).scale(0.7).move_to(server).shift(DOWN * 0.55)
        # self.add(txtClient, txtServer)
        # self.wait(0.1)
        # self.remove(txtClient, txtServer)
        # self.wait(0.1)
        # txtClient.set_color(GREY_B)
        # txtServer.set_color(GREY_B)
        # self.add(txtClient, txtServer)
        self.play(Write(txtClient), Write(txtServer))
        self.wait(0.5)
        self.play(txtClient.animate.set_color(GREY_B), txtServer.animate.set_color(GREY_B))
        self.play(*[mobj.animate.shift(LEFT * 3) for mobj in [txtClient, txtServer, clients, server]])

        t2c = { "UDP": MAROON_D, "TCP": GREEN_D, "255.255.255.255": BLUE_D, "教师端": BLUE_D, "考生端": BLUE_D }
        txt2 = Text("考生端在连接前，需要搜索教师端进行中的考试", t2c = t2c, color = GREY_D)
        txt3 = Text("首先，向 255.255.255.255 发送搜索考试的UDP广播消息", t2c = t2c, color = GREY_D)
        txt4 = Text("教师端接收到该广播消息后，随即通过UDP", t2c = t2c, color = GREY_D)
        txt5 = Text("传回自己的TCP地址和端口，以供考生端连接", t2c = t2c, color = GREY_D)
        txt6 = Text("随后考生端便可以在下拉列表中看到可供连接的考试", t2c = t2c, color = GREY_D)
        vgTxt2_6 = VGroup(txt2, txt3, txt4, txt5, txt6).scale(0.6).arrange(DOWN).to_edge(RIGHT)
        def circle_spread_animate():
            circle = Circle().move_to(clients[1][0]).set_stroke(MAROON_D, 1, 1).set_fill(opacity = 0)
            circle.generate_target()
            circle.scale(0)
            circle.target.scale(4).set_stroke(opacity = 0)
            return MoveToTarget(circle, rate_func = rush_into)
        circleIncidate = Circle(radius = 0.7).move_to(server).set_stroke(opacity = 0).set_fill(YELLOW, 0.3)
        lineUdp = DashedLine(server, clients[1][0], color = MAROON_D, width = 4)
        circleClient = Circle(radius = 0.6).move_to(clients[1][0]).set_stroke(YELLOW, 8, 0.3).set_fill(opacity = 0)
        self.play(Write(txt2))
        self.play(
            AnimationGroup(
                AnimationGroup(Write(txt3), *[clientsall[i].animate.set_stroke(opacity = 0.4) for i in range(len(clientsall)) if i != 3]), 
                AnimationGroup(*[circle_spread_animate() for _ in range(10)], lag_ratio = 0.1), 
                lag_ratio = 0.8
                )
            )
        self.play(FadeIn(circleIncidate, scale = 0.5), Write(txt4))
        self.play(AnimationGroup(Write(txt5), FadeOut(circleIncidate), GrowArrow(lineUdp), lag_ratio = 0.6))
        self.play(AnimationGroup(AnimationGroup(lineUdp.animate.scale(0, about_point = lineUdp.get_end()), ShowCreation(circleClient)), Write(txt6), lag_ratio = 0.6))
        self.wait(2)

        txt7 = Text("当加入考试时，考生端通过先前得到的地址和端口", t2c = t2c, color = GREY_D)
        txt8 = Text("即可通过TCP连接和教师端建立稳定连接", t2c = t2c, color = GREY_D)
        vgTxt7_8 = VGroup(txt7, txt8).scale(0.6).arrange(DOWN).to_edge(RIGHT)
        lineConnection = Line(clients[1][0], server, color = GREEN_D, width = 4)
        self.play(FadeOut(circleClient, run_time = 0.3), FadeOut(vgTxt2_6, run_time = 0.3), Write(txt7))
        self.wait(0.5)
        self.play(AnimationGroup(Write(txt8), GrowArrow(lineConnection), lag_ratio = 0.5))
        self.wait()
        self.play(*map(FadeOut, (txt1, clients, server, txtClient, txtServer, vgTxt7_8, lineConnection)))


        



        
