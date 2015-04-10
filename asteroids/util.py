
# class Keys(object):
    
#     def __init__(self):
#         self.map = {}
        
#     def put(self, key, value):
#         self.map[key] = value
        
#     def is_key_down(self, key):
#         val = self.map.get(key)
#         if val != None:
#             return val
#         else:
#             return False

class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        
class Dimension(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def set(self, width, height):
        self.width = width
        self.height = height

    def tuple(self):
        return (self.width, self.height)
        
class Rectangle(object):
    
    def __init__(self, x, y, width, height):
        self.pos = Point(x, y)
        self.size = Dimension(width, height)
        
def wrap_x(sprite):
    x = sprite.pos.x
    if x >= 0 and x <= ScreenSize.width:
        return x
    if x < -sprite.radius:
        return ScreenSize.width + sprite.radius
    elif x > ScreenSize.width + sprite.radius:
        return -sprite.radius
    else:
        return x
        
def wrap_y(sprite):
    y = sprite.pos.y
    if y >= 0 and y <= ScreenSize.height:
        return y
    if y < -sprite.radius:
        return ScreenSize.height + sprite.radius
    elif y > ScreenSize.height + sprite.radius:
        return -sprite.radius
    else:
        return y

ScreenSize = Dimension(700, 400)
