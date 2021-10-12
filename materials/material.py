from libs import zmath as zm

class Material(object):
    def __init__(self, diffuse, spec, texture):
        # diffuse = color de la superficie
        self.diffuse = diffuse
        self.spec = spec
        self.texture = texture
        # Luces
        self.ambientLight = None
        self.directionalLight = None
        self.pointLights = None
        self.intersect = None
        self.camPosition = None
        self.scene = None

    def objectLightning(self, scene, intersect):
        self.scene = scene
        self.ambientLight = scene.ambientLight
        self.directionalLight = scene.directionalLight
        self.pointLights = scene.pointLights
        self.intersect = intersect
        self.camPosition = scene.camPosition

    def getSpecular(self):
        specularIntensity = [0, 0, 0]
        directionalSpecular = self.directionalLight.getSpecular(self.intersect, self.camPosition, self.scene)

        for pointLight in self.pointLights:
            specular = pointLight.getSpecular(self.intersect, self.camPosition, self.scene)
            specularIntensity = zm.sum(specularIntensity, specular)

        specularIntensity = zm.sum(specularIntensity, directionalSpecular)
        return specularIntensity

    def getColor(self, direction, recursion):
        pass

    def textureColor(self):
        if self.texture and self.intersect.textCoords:
            textColor = self.texture.getColor(self.intersect.textCoords[0], self.intersect.textCoords[1])
            textColor = [textColor[2] / 255,
                         textColor[1] / 255,
                         textColor[0] / 255]
            return textColor
        else:
            return [1, 1, 1]

