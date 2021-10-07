from materials.material import Material
import libs.zutils as zu

class Reflective(Material):

    def __init__(self, diffuse=zu.WHITE, spec=1, texture=None):
        super().__init__(diffuse, spec, texture)

    def getColor(self, direction, recursion):
        reflect = zu.reflection(self.intersect.normal, [-i for i in direction])
        reflectColor = self.scene.castRay(self.intersect.point, reflect, self.intersect.figure, recursion + 1)
        intensity = [reflectColor[2] / 255,
                     reflectColor[1] / 255,
                     reflectColor[0] / 255]

        return intensity
