from libs.zutils import V3, WHITE

class AmbientLight:
    def __init__(self, strength=0, color=WHITE):
        self.strength = strength
        self.color = color

    def getColor(self):
        ambient = [self.strength * self.color[2] / 255,
                   self.strength * self.color[1] / 255,
                   self.strength * self.color[0] / 255]
        return ambient