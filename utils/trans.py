from manimlib import Text, VMobject

def txtmobj2vmobj(txt: Text, *args, **kwargs):
    m = VMobject(*args, **kwargs)
    txt.get_points
    points = []
    for sub in txt:
        points.extend(sub.get_points())
    m.set_points(points)
    return m

def num2hex(num):
    return chr(ord('0') + num) if num < 10 else chr(ord('A') + (num - 10))
