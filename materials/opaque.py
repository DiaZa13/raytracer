from materials.material import Material
import libs.zutils as zu
import libs.zmath as zm


class Opaque(Material):

    def __init__(self, diffuse=zu.WHITE, spec=1, texture=None):
        super().__init__(diffuse, spec, texture)

    def getColor(self, direction, recursion):
        intensity = [0, 0, 0]

        if self.ambientLight:
            intensity = zm.sum(intensity, self.ambientLight.getColor())

        if self.directionalLight:
            directionalIntensity = self.directionalLight.getDiffuse()
            intensity = zm.sum(intensity, directionalIntensity)

        for pointLight in self.pointLights:
            pointLightIntensity = pointLight.getDiffuse()
            intensity = zm.sum(intensity, pointLightIntensity)

        return intensity


