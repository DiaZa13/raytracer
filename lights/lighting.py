import libs.zmath as zm
import libs.zutils as zu

class Light(object):
    def __init__(self, light, intersect, light_direction):
        self.light = light
        self.intersect = intersect
        self.material = intersect.figure.material
        self.light_direction = light_direction

    def diffuse(self):
        intensity = max(0, zm.dot(self.intersect.normal, self.light_direction)) * self.light.intensity
        diffuse = [intensity * self.light.color[2] / 255,
                   intensity * self.light.color[1] / 255,
                   intensity * self.light.color[0] / 255]
        return diffuse

    def specular(self, camPosition):
        view_direction = zm.subtract(camPosition, self.intersect.point)
        view_direction = zm.normalize(view_direction)
        # Vector de la luz reflejada → R = 2 * (normal • lights) * normal - lights
        reflect = zu.reflection(self.intersect.normal, self.light_direction)
        intensity = self.light.intensity * pow((max(0, zm.dot(view_direction, reflect))), self.material.spec)
        specular = [intensity * self.light.color[2] / 255,
                    intensity * self.light.color[1] / 255,
                    intensity * self.light.color[0] / 255]
        return specular








