# Figuras para las intersecciones
import libs.zmath as zm
from libs.zutils import V3
from numpy import arctan2, arccos


class Intersect(object):
    def __init__(self, distance, point, normal, figure, textCoords):
        # distance = distancia a la que hace contacto
        self.distance = distance
        self.point = point
        self.normal = normal
        self.textCoords = textCoords
        self.figure = figure




class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def rayIntersect(self, origin, direction):
        # P = O + t * D
        # O = origen
        # t = distancia recorrida
        # D = dirección del rayo
        L = zm.subtract(self.center, origin)
        # Tca = distancia perpendicular del origen al centro
        tca = zm.dot(L, direction)
        # Magnitud de L
        # Implementar calculo de magnitud
        l = zm.hypotenuse(L)

        d = (l ** 2 - tca ** 2) ** 0.5
        # d = punto perpendicular más cercano al centro de la esfera

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        # La cámara está dentro de la esfera (están en la misma posición)
        # La esfera está detrás de la cámara
        if t0 < 0:
            if t1 < 0:
                return None
            else:
                t0 = t1

        # Intersect point
        # Agregar a mi librería la multiplicación de escalar por vector
        hit = zm.sum(origin, V3(t0 * direction[0],
                                t0 * direction[1],
                                t0 * direction[2]))
        # Normal
        normal = zm.subtract(hit, self.center)
        # Asegurar normalizar la normal
        normal = zm.normalize(normal)

        u = 1 - (arctan2(normal[2], normal[0]) / (2 * zm.pi()) + 0.5)
        v = arccos(-normal[1]) / zm.pi()
        uvs = (u, v)

        return Intersect(distance=t0, point=hit, normal=normal, figure=self, textCoords=uvs)

class Plane(object):
    # Normal → dirección a dónde está viendo el plano
    # Este será un plano infinito
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = zm.normalize(normal)
        self.material = material

    # El rayo no hace contacto si:
    # * Es paralelo
    # * Si el punto de origen es arriba/abajo del plano y va hacia afuera
    def rayIntersect(self, origin, direction):
        # t = ((planePos - ray_origin) dot plane_normal) / ray_direction dot plane_normal
        denom = zm.dot(direction, self.normal)

        if abs(denom) > 0.0001:
            t = (zm.dot(zm.subtract(self.position, origin), self.normal)) / denom
            # Distancia con la que hace contacto con el plano, pero no toma en cuenta si está atrás
            # Si t es negativo → no hay contacto con el plano
            if t > 0:
                # P = O + t * D → punto de contacto
                hit = zm.sum(origin, zm.multiply(t, direction))

                return Intersect(distance=t, point=hit, normal=self.normal, figure=self, textCoords=None)

        # Cuando el valor es 0 el rayo es perpendicular al plano
        # O cuando t es negativo
        return None

class AABB(object):
    # Axis Aligned Bounding Box → no se puede rotar
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material
        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]
        self.planes = []

        halfSize = [size[0] / 2, size[1] / 2, size[2] / 2]
        right = zm.sum(position, V3(halfSize[0], 0, 0))
        left = zm.sum(position, V3(-halfSize[0], 0, 0))
        up = zm.sum(position, V3(0, halfSize[1], 0))
        down = zm.sum(position, V3(0, -halfSize[1], 0))
        front = zm.sum(position, V3(0, 0, halfSize[2]))
        back = zm.sum(position, V3(0, 0, -halfSize[2]))

        # Lados
        self.planes.append(Plane(right, V3(1, 0, 0), material))
        self.planes.append(Plane(left, V3(-1, 0, 0), material))
        # Arriba/abajo
        self.planes.append(Plane(up, V3(0, 1, 0), material))
        self.planes.append(Plane(down, V3(0, -1, 0), material))
        # Adelante/atrás
        self.planes.append(Plane(front, V3(0, 0, 1), material))
        self.planes.append(Plane(back, V3(0, 0, -1), material))

        # Bounds
        epsilon = 0.001
        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + self.size[i]/2)
            self.boundsMax[i] = self.position[i] + (epsilon + self.size[i]/2)

    def rayIntersect(self, origin, direction):
        intersect = None
        t = float('inf')

        uvs = None

        for plane in self.planes:
            planeInter = plane.rayIntersect(origin, direction)

            if planeInter:
                # Revisa que esté dentro de los borders
                if self.boundsMin[0] <= planeInter.point[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planeInter.point[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planeInter.point[2] <= self.boundsMax[2]:
                            if planeInter.distance < t:
                                # Revisar el plano con el cual hace primero contacto
                                intersect = planeInter
                                t = planeInter.distance

                                u, v = 0, 0
                                if abs(plane.normal[0]) > 0:  # está viendo a los lados
                                    # Necesito las coordenadas en Y y Z
                                    u = (planeInter.point[1] - self.boundsMin[1]) / (self.boundsMax[1] - self.boundsMin[1])
                                    v = (planeInter.point[2] - self.boundsMin[2]) / (self.boundsMax[2] - self.boundsMin[2])
                                elif abs(plane.normal[1]) > 0:  # está viendo hacia arriba/abajo
                                    # Necesito las coordenadas en X y Z
                                    u = (planeInter.point[0] - self.boundsMin[0]) / (self.boundsMax[0] - self.boundsMin[0])
                                    v = (planeInter.point[2] - self.boundsMin[2]) / (self.boundsMax[2] - self.boundsMin[2])
                                elif abs(plane.normal[2]) > 0:  # está viendo hacia adelante/atrás
                                    # Necesito las coordenadas en X y Y
                                    u = (planeInter.point[0] - self.boundsMin[0]) / (self.boundsMax[0] - self.boundsMin[0])
                                    v = (planeInter.point[1] - self.boundsMin[1]) / (self.boundsMax[1] - self.boundsMin[1])

                                uvs = (u, v)

        if intersect is None:
            return None

        return Intersect(distance=intersect.distance, point=intersect.point, normal=intersect.normal, figure=self, textCoords=uvs)





