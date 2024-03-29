import sys
sys.path.append('.')
from manimlib import *
from utils.header_legacy import *

'''
PhyElecF_TitleScene:
    视频标题
PhyElecF_LineChapterScene:
    Part 1: 磁场中的通电直导线
PhyElecF_LineScene:
    我们知道，两个相对的异名磁极之间会形成所示磁场
    **演示，GrowArrow**
    **切换视角**
    对于穿过其中的一段平行的通电直导线，将会受到安培力的作用
'''

class FaceTakedCube(Cube):
    CONFIG = { 
        "take_faces": (0, 0, 0, 0, 0, 0)
    }
    takemaps = (
        ((1, 4), (4, 3), (2, 1), (3, 2)),
        ((5, 4), (4, 0), (2, 5), (0, 2)),
        ((1, 0), (0, 3), (5, 1), (3, 5)),
        ((0, 4), (4, 5), (2, 0), (5, 2)),
        ((1, 5), (5, 3), (0, 1), (3, 0)),
        ((3, 4), (4, 1), (2, 3), (1, 2))
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(6):
            face = self[i]
            if self.take_faces[i]:
                face.set_opacity(0)
                continue
            takemap = self.takemaps[i]
            face.set_opacity([
                not any(
                    [self.take_faces[depend] for depend in vertex]
                ) for vertex in takemap
            ])

class PhyElecF_TitleScene(Scene):
    def construct(self):
        self.add(txtwatermark())
        txt = Text("【物理】通电导线、磁场与左手定则", t2c = { "【物理】": BLUE }).scale(1.4)
        self.play(DrawBorderThenFill(txt))
        self.wait()
        self.play(FadeOut(txt))

class PhyElecF_LineChapterScene(ChapterScene):
    CONFIG = {
        "str1": "Part 1",
        "str2": "磁场中的通电直导线"
    }

class PhyElecF_LineScene(Scene):
    def construct(self):
        frame = self.camera.frame

        frame.set_euler_angles(
            theta = 0,
            phi = 90 * DEGREES,
            gamma = -90 * DEGREES
        ).set_width(frame.get_width() * 1.2)
        frame.focal_distance = 100
        focal_distance_tracker = ValueTracker(100)
        def frame_updater(m):
            m.focal_distance = focal_distance_tracker.get_value()
        frame.add_updater(frame_updater)

        self.add(txtwatermark().fix_in_frame())
        cubeN = FaceTakedCube(color = RED, gloss = 0, shadow = 0, take_faces = (1, 0, 0, 0, 0, 0))\
            .next_to(ORIGIN, OUT, buff = 3).stretch(2, 0).stretch(2, 1)
        cubeS = FaceTakedCube(color = BLUE, gloss = 0, shadow = 0, take_faces = (0, 0, 0, 0, 0, 1))\
            .next_to(ORIGIN, IN, buff = 3).stretch(2, 0).stretch(2, 1)
        self.add(cubeN, cubeS, ThreeDBorder(cubeN, color = BLACK, width = 0.025), ThreeDBorder(cubeS, color = BLACK, width = 0.025))
        self.add(Arrow(OUT * 3, IN * 3).apply_depth_test())
        self.wait()
        self.play(
            focal_distance_tracker.animate.set_value(2),
            frame.animate.set_euler_angles(theta = 20 * DEGREES, phi = 70 * DEGREES, gamma = 0),
            run_time = 2)
        self.wait()

class TestScene(Scene):
    def construct(self):
        frame = self.camera.frame

        frame.set_euler_angles(
            theta = 0,
            phi = 90 * DEGREES,
            gamma = -90 * DEGREES
        ).set_width(frame.get_width() * 1.2)
        frame.focal_distance = 100
        focal_distance_tracker = ValueTracker(100)
        def frame_updater(m):
            m.focal_distance = focal_distance_tracker.get_value()
        frame.add_updater(frame_updater)

        # self.add(txtwatermark().fix_in_frame())
        cubeN = FaceTakedCube(color = RED, gloss = 0, shadow = 0, take_faces = (1, 0, 0, 0, 0, 0))\
            .next_to(ORIGIN, OUT, buff = 3).stretch(2, 0).stretch(2, 1)
        cubeS = FaceTakedCube(color = BLUE, gloss = 0, shadow = 0, take_faces = (0, 0, 0, 0, 0, 1))\
            .next_to(ORIGIN, IN, buff = 3).stretch(2, 0).stretch(2, 1)
        self.add(cubeN, cubeS, ThreeDBorder(cubeN, color = BLACK, width = 0.025), ThreeDBorder(cubeS, color = BLACK, width = 0.025))
        self.add(Arrow(OUT * 3, IN * 3).apply_depth_test())
        self.wait()
        self.play(
            focal_distance_tracker.animate.set_value(2),
            frame.animate.set_euler_angles(theta = 20 * DEGREES, phi = 70 * DEGREES, gamma = 0),
            run_time = 2)
        self.wait()
        
