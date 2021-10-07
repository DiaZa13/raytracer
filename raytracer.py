# Graphic library

from collections import namedtuple
from libs import zutils as zu
from libs import zmath as zm
from libs.obj import Obj
from numpy import tan
from materials.transparent import Transparent

# Creación de un tipo de variable para dibujar una línea
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

# COLORS
BLACK = zu.colors(0, 0, 0)
WHITE = zu.colors(1, 1, 1)

MAX_RECURSION_DEPTH = 3
STEPS = 1


# Creación de clase para hacer renderizar
class Raytracer(object):
    def __init__(self, width, height):  # constructor
        # Las variables se crean dentro del constructor
        self.draw_color = WHITE
        self.clear_color = BLACK
        # Window size
        self.width = width
        self.height = height
        self.createWindow()
        self.camPosition = V3(0, 0, 0)
        self.fov = 60

        # Agrega los objetos que se quieren renderizar en pantalla
        self.scene = []
        self.ambientLight = None
        self.directionalLight = None
        self.pointLights = []

        self.envmap = None

    # -------- CLEAR
    # Define el color con el que se va a limpiar la pantalla
    def clearColor(self, r, g, b):
        self.clear_color = zu.colors(r, g, b)

    # Limpiar pixeles de la pantalla (ponerlos todos en blanco o negro)
    def clear(self):
        # Estructura para almacenar los pixeles de 2D para limpiar pantalla
        self.pixels = [[self.clear_color for y in range(self.height)] for x in range(self.width)]

    # Creación de la ventana
    def createWindow(self):
        self.clear()
        # Default viewport
        self.viewport(self.width, self.height, 0, 0)

    # Viewport
    def viewport(self, width, height, x, y, color=None):
        self.vw_width = int(width - 1)
        self.vw_height = int(height - 1)
        self.vw_x = int(x)
        self.vw_y = int(y)

        for a in range(int(x), (self.vw_width + int(x) + 1)):
            for b in range(int(y), (self.vw_height + int(y) + 1)):
                self.pixels[a][b] = color or self.clear_color

    # --------- DRAW
    def drawColor(self, r, g, b):
        self.draw_color = zu.colors(r / 255, g / 255, b / 255)

    def drawPoint(self, x, y, color=None):
        if x < self.vw_x or x > self.vw_x + self.vw_width or y < self.vw_y or y > self.vw_y + self.vw_height:
            print('test')
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.draw_color

    def loadModel(self, filename, scale=V3(1, 1, 1), translate=V3(0, 0, 0), rotate=V3(0, 0, 0)):

        model = Obj(filename)
        modelMatrix = self.objectMatriz(translate, scale, rotate)
        rotationMatrix = self.CreateRotationMatrix(rotate)

        # draw Model
        for face in model.faces:
            vertex_count = len(face)  # Guarda la cantidad de vertices en la cara

            # Vértices transformados por la matriz del modelo
            vert, vt, vn = [], [], []
            for i in range(vertex_count):
                vertex = model.vertices[face[i][0] - 1]
                a = self.transform(vertex, modelMatrix)
                vert.append(a)
                # Coordenadas de textura
                vt.append(model.textures[face[i][1] - 1])
                # Normales
                # Las normales que devuelve el modelo son antes de haber
                # rotado el objeto. Para tener las normales correctas
                # hay que asegurar que también están rotadas
                normal = model.normals[face[i][2] - 1]
                a = self.transform_direction(normal, rotationMatrix)
                vn.append(a)

            # Transformación de vértices por la cámara
            a = self.camTransform(vert[0])
            b = self.camTransform(vert[1])
            c = self.camTransform(vert[2])
            if vertex_count == 4:
                d = self.camTransform(vert[3])

            # Dibuja los vértices
            self.drawTriangle_bc(a, b, c, textCoords=(vt[0], vt[1], vt[2]), normals=(vn[0], vn[1], vn[2]),
                                 vertx=(vert[0], vert[1], vert[2]))

            if vertex_count == 4:
                self.drawTriangle_bc(a, c, d, textCoords=(vt[0], vt[2], vt[3]), normals=(vn[0], vn[2], vn[3]),
                                     vertx=(vert[0], vert[1], vert[2]))

    def render(self):
        for y in range(0, self.height, STEPS):
            for x in range(0, self.width, STEPS):  # Convertir de world coordinates a NCD
                px = 2 * ((x + 1 / 2) / self.width) - 1  # Se le suma 1/2 al pixel para que al momento de generar los
                py = 2 * ((
                                  y + 1 / 2) / self.height) - 1  # rayos desde los pixeles el mismo se genere desde en el centro
                # Simulación del ángulo de visión, asumiendo que el near plane está a 1 unidad de la cámara
                aRatio = self.width / self.height
                t = tan(zm.deg2rad(self.fov) / 2)
                r = t * self.width / self.height
                # Calcular posición de los pixeles en un espacio 3D
                px *= r
                py *= t

                # Dirección del rayo
                # La cámara siempre está viendo hacia -Z
                dirRay = V3(px, py, -1)
                dirRay = zm.normalize(dirRay)
                # El origen del rayo es la posición de la cámara
                self.drawPoint(x, y, self.castRay(self.camPosition, dirRay))

    def castRay(self, origin, direction, origin_object=None, recursion=0):
        intersect = self.sceneIntersect(origin, direction, origin_object)

        if intersect is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envmap:
                return self.envmap.getColor(direction)
            return self.clear_color

        # If intersect is not None
        material = intersect.figure.material
        material.objectLightning(self, intersect)
        color = [material.diffuse[2] / 255,
                 material.diffuse[1] / 255,
                 material.diffuse[0] / 255]

        specularIntensity = material.getSpecular()

        if isinstance(material, Transparent):
            # Fresnel
            # Qué tanta refracción y reflexión hay
            outside = zm.dot(direction, intersect.normal) < 0
            # Para que no haga contacto con la superficie de sí mismo, no se, se revisa a cierta distancia para que
            # no toque la superficie
            bias = zm.multiply(0.001, intersect.normal)
            kr = zu.fresnel(intersect.normal, direction, material.ior)

            reflect = zu.reflection(intersect.normal, [-i for i in direction])
            reflect_origin = zm.sum(bias, intersect.point) if outside else zm.subtract(intersect.point, bias)
            reflectColor = self.castRay(reflect_origin, reflect, None, recursion + 1)
            reflectColor = [reflectColor[2] / 255,
                            reflectColor[1] / 255,
                            reflectColor[0] / 255]
            intensity = zm.multiply(kr, reflectColor)

            if kr < 1:
                refract = zu.refractor(intersect.normal, direction, material.ior)
                refract_origin = zm.subtract(intersect.point, bias) if outside else zm.sum(bias, intersect.point)
                refractColor = self.castRay(refract_origin, refract, None, recursion + 1)
                refractColor = [refractColor[2] / 255,
                                refractColor[1] / 255,
                                refractColor[0] / 255]
                refractColor = zm.multiply((1 - kr), refractColor)
                intensity = zm.sum(intensity, refractColor)

            intensity = zm.sum(intensity, specularIntensity)
        else:
            intensity = material.getColor(direction, recursion)
            intensity = zm.sum(intensity, specularIntensity)
            textColor = material.textureColor()
            intensity = zm.multiply(intensity, textColor)

        r = min(1, color[0] * intensity[0])
        g = min(1, color[1] * intensity[1])
        b = min(1, color[2] * intensity[2])

        return zu.colors(r, g, b)

    # intensidad = dot(normalSuperficie, directionLuz)
    def sceneIntersect(self, origin, direction, origin_object=None):
        depth = float("inf")
        intersect = None
        for figure in self.scene:
            if figure is not origin_object:
                hit = figure.rayIntersect(origin, direction)
                if hit is not None:
                    # z-buffer
                    if hit.distance < depth:
                        intersect = hit
                        depth = hit.distance

        return intersect

    '''
    Creación de bitmap
    @:arg filename: nombre del documento .bmp
    '''

    def end(self, filename):
        with open(filename, 'wb') as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            # 14 bytes del header + 40 InfoHeader + color table → ancho * altura * 3 (r,g,b) de cada uno
            file.write(zu.dword(14 + 40 + (self.width * self.height * 3)))
            # 4 bytes reservados vacíos
            file.write(zu.dword(0))
            file.write(zu.dword(14 + 40))
            # InfoHeader
            # Tamaño de infoHeader
            file.write(zu.dword(40))
            file.write(zu.dword(self.width))
            file.write(zu.dword(self.height))
            file.write(zu.word(1))
            file.write(zu.word(24))
            file.write(zu.dword(0))
            file.write(zu.dword(self.width * self.height * 3))
            file.write(zu.dword(0))
            file.write(zu.dword(0))
            file.write(zu.dword(0))
            file.write(zu.dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
