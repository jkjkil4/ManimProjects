def eqRange(fromValue, toValue, step = 1):
    value = fromValue
    while(value <= toValue):
        yield value
        value += step

def getPos(mobject):
    return [mobject.get_x(), mobject.get_y(), mobject.get_z()]
