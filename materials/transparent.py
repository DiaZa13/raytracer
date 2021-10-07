from materials.material import Material
import libs.zutils as zu
import libs.zmath as zm

class Transparent(Material):
    def __init__(self, diffuse=zu.WHITE, spec=1, texture=None, ior=1):
        super().__init__(diffuse, spec, texture)
        self.ior = ior

    def getColor(self, direction, recursion):
        # Fresnel
        # Qué tanta refracción y reflexión hay
        outside = zm.dot(direction, self.intersect.normal) < 0
        # Para que no haga contacto con la superficie de sí mismo, no se, se revisa a cierta distancia para que
        # no toque la superficie
        bias = zm.multiply(0.001, self.intersect.normal)
        kr = zu.fresnel(self.intersect.normal, direction, self.ior)

        reflect = zu.reflection(self.intersect.normal, [-i for i in direction])
        reflect_origin = zm.sum(bias, self.intersect.point) if outside else zm.subtract(self.intersect.point, bias)
        reflectColor = self.scene.castRay(reflect_origin, reflect, None, recursion + 1)
        reflectColor = [reflectColor[2] / 255,
                        reflectColor[1] / 255,
                        reflectColor[0] / 255]
        intensity = zm.multiply(kr, reflectColor)

        if kr < 1:
            refract = zu.refractor(self.intersect.normal, direction, self.ior)
            refract_origin = zm.subtract(self.intersect.point, bias) if outside else zm.sum(bias, self.intersect.point)
            refractColor = self.scene.castRay(refract_origin, refract, None, recursion + 1)
            refractColor = [refractColor[2] / 255,
                            refractColor[1] / 255,
                            refractColor[0] / 255]
            refractColor = zm.multiply((1 - kr), refractColor)
            intensity = zm.sum(intensity, refractColor)

        return intensity
