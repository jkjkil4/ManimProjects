from manimlib import *

frame_path = 'C:\\Users\\jkjki\\Desktop\\Projects\\Other\\2022-1-15 Bad-Apple\\frame.png'

class CDRect(Rectangle):
    def __init__(self, UL, DR, **kwargs):
        super().__init__(DR[0] - UL[0], DR[1] - UL[1], **kwargs)
        self.move_to((UL + DR) / 2)

class Scene1(Scene):
    def construct(self):
        img = ImageMobject(frame_path)
        img.scale(FRAME_WIDTH / img.get_width())
        self.add(img)
        img.add_mouse_press_listner(lambda mobj, pos: print(mobj, pos))

        rect_buzzer = CDRect(np.array([-5.55, -2.99, 0]), np.array([-4.57, -3.85, 0]))
        rect_buzzer.set_stroke(YELLOW, 4).set_fill(opacity = 0)
        rect_lcd = CDRect(np.array([-2.47, -1.94, 0]), np.array([ 1.62, -3.31, 0]))
        rect_lcd.set_stroke(YELLOW, 4).set_fill(opacity = 0)

        txt_buzzer = Text("蜂鸣器").scale(0.8).next_to(rect_buzzer, UP)

        self.play(ShowCreation(rect_buzzer), Write(txt_buzzer))

        self.interact()
