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
