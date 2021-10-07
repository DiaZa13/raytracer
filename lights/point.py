from lights.lighting import Light
import libs.zmath as zm
from libs.zutils import V3, WHITE

class PointLight(object):
    # Es una luz con un punto de origen que se esparce a todas las direcciones
    # "genera" una cantidad infinita de rayos de luz en todas las direcciones
    def __init__(self, position=V3(0, 0, 0), intensity=1, color=WHITE):
        self.position = position
        self.intensity = intensity
        self.color = color
        self.intersect = None
        self.shadow = None
        self.light = None

    def getSpecular(self, intersect, camPosition, scene):
        self.intersect = intersect
        self.shadow = self.shadowCalc(scene)
        light_direction = zm.subtract(self.position, self.intersect.point)
        light_direction = zm.normalize(light_direction)
        self.light = Light(self, intersect, light_direction)
        specular = self.light.specular(camPosition)
        specular = zm.multiply(self.shadow, specular)

        return specular

    def shadowCalc(self, scene):
        light_direction = zm.subtract(self.position, self.intersect.point)
        light_direction = zm.normalize(light_direction)
        shadow_intensity = 0
        shadow_intersect = scene.sceneIntersect(self.intersect.point, light_direction, self.intersect.figure)
        light_distance = zm.subtract(self.position, self.intersect.point)
        light_distance = zm.hypotenuse(light_distance)

        if shadow_intersect and shadow_intersect.distance < light_distance:
            shadow_intensity = 1

        return 1 - shadow_intensity

    def getDiffuse(self):
        diffuse = self.light.diffuse()
        diffuse = zm.multiply(self.shadow, diffuse)

        return diffuse
