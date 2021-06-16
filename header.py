def eqRange(fromValue, toValue, step = 1):
    value = fromValue
    while(value <= toValue):
        yield value
        value += step

def getPos(mobject):
    return [mobject.get_x(), mobject.get_y(), mobject.get_z()]
    
def getLineCenter(line):    # 用于得到线段中点
    return (line.get_start() + line.get_end()) / 2
def getLineLerp(line, k):
    return line.get_start() * (1 - k) + line.get_end() * k