import libs.zmath as zm
from libs.zutils import V3
from polygons.polygons import Intersect


class Cone(object):
    def __init__(self, tip, angle, axis, height, material):
        self.tip = tip  # c
        self.angle = angle  # cosa
        self.axis = zm.normalize(axis)  # v
        self.height = height # h
        self.material = material

    '''
    @author: Julien Guertault
    Extraído de: https://lousodrome.net/blog/light/2017/01/03/intersection-of-a-ray-and-a-cone/
    Adaptado por: Diana Corado
    '''
    def rayIntersect(self, origin, direction):
        # P = O + t * D
        # ((P - C) • V2)^2 - (P - C)cos^2(angle) = 0
        # O = origen
        # t = distancia recorrida
        # D = dirección del rayo

        co = zm.subtract(origin, self.tip)

        da = zm.dot(direction, self.axis)
        coa = zm.dot(co, self.axis)
        dco = zm.dot(direction, co)
        coco = zm.dot(co, co)

        a = da ** 2 - self.angle ** 2
        b = 2 * (da * coa - dco * self.angle ** 2)
        c = coa ** 2 - coco * self.angle ** 2

        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return None

        discriminant = pow(discriminant, 0.5)
        t0 = (-b - discriminant) / (2 * a)
        t1 = (-b + discriminant) / (2 * a)

        if t0 > t1:
            t0, t1 = t1, t0

        if t0 < 0:
            if t1 < 0:
                return None
            else:
                t0 = t1

        ha = zm.multiply(t0, direction)
        ha = zm.sum(origin, ha)
        hit = zm.subtract(ha, self.tip)
        h = zm.dot(hit, self.axis)
        if h < 0 or h > self.height:
            return None

        d = zm.dot(self.axis, hit)
        e = zm.dot(hit, hit)
        f = zm.multiply(d, hit)
        g = zm.subtract(e, self.axis)
        normal = zm.divide(f, g)
        normal = zm.normalize(normal)

        return Intersect(distance=t0, point=hit, normal=normal, figure=self, textCoords=None)
