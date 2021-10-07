from lights.lighting import Light
from libs.zutils import V3, WHITE
import libs.zmath as zm


class DirectionalLight(object):
    def __init__(self, direction=V3(0, -1, 0), intensity=1, color=WHITE):
        self.direction = zm.normalize(direction)
        self.light_direction = [-i for i in self.direction]
        self.intensity = intensity
        self.color = color
        self.intersect = None
        self.shadow = None
        self.light = None

    def getSpecular(self, intersect, camPosition, scene):
        self.intersect = intersect
        self.shadow = self.shadowCalc(scene)
        self.light = Light(self, self.intersect, self.light_direction)
        specular = self.light.specular(camPosition)
        specular = zm.multiply(self.shadow, specular)

        return specular

    def shadowCalc(self, scene):
        shadow_intensity = 0
        shadow_intersect = scene.sceneIntersect(self.intersect.point, self.light_direction, self.intersect.figure)
        if shadow_intersect:
            shadow_intensity = 1

        return 1 - shadow_intensity

    def getDiffuse(self):
        diffuse = self.light.diffuse()
        diffuse = zm.multiply(self.shadow, diffuse)

        return diffuse
