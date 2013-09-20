# Author: Jonathan Jengo

ScreenSize = (700, 400)

# Holds a map of key states
class Keys:
    
    # Initialize
    def __init__(self):
        self.map = {}
        
    # Add key map entry
    def put(self, key, value):
        self.map[key] = value
        
    # Return if a key is down
    def isKeyDown(self, key):
        val = self.map.get(key)
        if val != None:
            return val
        else:
            return False

# Represents a [x,y] coordinate
class Point:
    
    # Initialize
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Set the [x,y] point
    def move(self, x, y):
        self.x = x
        self.y = y
        
    # Move the point by delta
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        
# Represents a size abstraction
class Dimension:
    
    # Initialize
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    # Set the dimension size
    def set(self, width, height):
        self.width = width
        self.height = height
        
# Represents a bounds abstraction
class Rectangle:
    
    # Initialize
    def __init__(self, x, y, width, height):
        self.pos = Point(x, y)
        self.size = Dimension(width, height)
        
def wrapX(x, sprite):
    
    if x >= 0 and x <= ScreenSize[0]:
        return x

    if x < -sprite.radius:
        return ScreenSize[0] + sprite.radius
    elif x > ScreenSize[0] + sprite.radius:
        return -sprite.radius
    else:
        return x
        
def wrapY(y, sprite):
    
    if y >= 0 and y <= ScreenSize[1]:
        return y
    
    if y < -sprite.radius:
        return ScreenSize[1] + sprite.radius
    elif y > ScreenSize[1] + sprite.radius:
        return -sprite.radius
    else:
        return y
