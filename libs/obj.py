# Cargar archivo OBJ
import struct
from libs.zutils import colors
from libs.zmath import normalize, pi
from numpy import arccos, arctan2


def color(r, g, b):
    # Comúnmente la tarjeta de video en colores acepta valor de 0 a 1
    # Y para convertirlo en byte se multiplica por 255
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:  # Por default open ya está en read-text
            self.lines = file.read().splitlines()  # Lee el documento línea por línea

        # Variables para almacenar la lectura del documento
        self.vertices = []
        self.textures = []  # Coordenadas de texturas
        self.textures2 = []
        self.normals = []
        self.normals2 = []
        self.faces = []

        self.saveData()

    def saveData(self):
        # Formato de OBJ
        # v -0.8523 -0.6325 -0.5238 → letra = prefijo, valores = coordenadas
        newTexture = False
        for line in self.lines:
            # Asegurar que la línea no está en blanco
            if line:
                prefix, value = line.split(' ', 1)  # Separar el prefijo del valor
                if prefix == 'v':  # Vertices
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':  # Coordenadas de textura
                    if not newTexture:
                        self.textures.append(list(map(float, value.split(' '))))
                    elif newTexture:
                        self.textures2.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':  # Normales
                    if not newTexture:
                        self.normals.append(list(map(float, value.split(' '))))
                    elif newTexture:
                        self.normals2.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(int, vertex.split('/'))) for vertex in value.split(' ')])
                elif prefix == 'o':
                    newTexture = True


# Implementar texturas
class Texture(object):
    def __init__(self, filename):
        self.file = filename
        self.read()

    def read(self):
        # rb → abrir el archivo en modo lectura binario
        with open(self.file, 'rb') as img:
            img.seek(10)  # Se salta 10bytes
            headerSize = struct.unpack('=l', img.read(4))[0]  # Para que lea el size del header

            img.seek(14 + 4)  # Se mueve a la posición en la que esta el ancho y el alto
            self.width = struct.unpack('=l', img.read(4))[0]  # Lee los 4bytes correspondientes del ancho
            self.height = struct.unpack('=l', img.read(4))[0]  # Lee los 4bytes correspondientes de la altura

            # Se necesitaba para empezar a leer la tabla de colores de la textura
            img.seek(headerSize)
            # Empezar a leer la imagen
            self.pixels = []  # Array de pixeles
            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    # Leyendo los colores de la textura
                    b = ord(img.read(1)) / 255  # ord → convierte el caracter a ascii
                    g = ord(img.read(1)) / 255  # /255 para asegurar que el valor va de 0-1
                    r = ord(img.read(1)) / 255
                    self.pixels[y].append(colors(r, g, b))

    def getColor(self, tx, ty):
        if 0 <= tx < 1 and 0 <= ty < 1:
            # Porque las coordenadas de color no están normalizadas
            x = int(tx * self.width)
            y = int(ty * self.height)
            if self.pixels[y][x]:
                return self.pixels[y][x]
            else:
                return colors(0, 0, 0)
        else:
            # Si se pasan coordenas inválidas entonces se devuelve negro
            return colors(0, 0, 0)


# Enviroment map
class EnvMap(object):
    def __init__(self, filename):
        self.file = filename
        self.read()

    def read(self):
        # rb → abrir el archivo en modo lectura binario
        with open(self.file, 'rb') as img:
            img.seek(10)  # Se salta 10bytes
            headerSize = struct.unpack('=l', img.read(4))[0]  # Para que lea el size del header

            img.seek(14 + 4)  # Se mueve a la posición en la que esta el ancho y el alto
            self.width = struct.unpack('=l', img.read(4))[0]  # Lee los 4bytes correspondientes del ancho
            self.height = struct.unpack('=l', img.read(4))[0]  # Lee los 4bytes correspondientes de la altura

            # Se necesitaba para empezar a leer la tabla de colores de la textura
            img.seek(headerSize)
            # Empezar a leer la imagen
            self.pixels = []  # Array de pixeles
            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    # Leyendo los colores de la textura
                    b = ord(img.read(1)) / 255  # ord → convierte el caracter a ascii
                    g = ord(img.read(1)) / 255  # /255 para asegurar que el valor va de 0-1
                    r = ord(img.read(1)) / 255
                    self.pixels[y].append(colors(r, g, b))

    def getColor(self, direction):
        direction = normalize(direction)
        x = int((arctan2(direction[2], direction[0]) / (2 * pi()) + 0.5) * self.width)
        y = int(arccos(-direction[1]) / pi() * self.height)

        return self.pixels[y][x]
