# Librería de operaciones matemáticas
from collections import namedtuple
import numpy as np

V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

# Resta de 2 vectores
def subtract(v1, v2):
    result = []

    if isinstance(v2, (float, int)):
        for i in range(len(v1)):
            result.append(v1[i] - v1)
    if len(v1) == len(v2):
        for i in range(len(v1)):
            result.append(v1[i] - v2[i])
    else:
        return

    return result

# Suma de 2 vectores
def sum(v1, v2):
    result = []

    if isinstance(v1, (float, int)):
        for i in range(len(v2)):
            result.append(v1 + v2[i])
    if isinstance(v2, (float, int)):
        for i in range(len(v1)):
            result.append(v1[i] + v2)
    elif len(v1) == len(v2):
        for i in range(len(v1)):
            result.append(v1[i] + v2[i])
    else:
        return

    return result

# Multiplicación entre 2 vectores
def multiply(a, b):
    result = []

    if isinstance(a, (float, int)):
        for i in range(len(b)):
            result.append(a * b[i])
    elif len(a) == len(b):
        for i in range(len(a)):
            result.append(a[i] * b[i])
    else:
        return

    return result


# Producto cruz entre 2 vectores
def cross(a, b):
    result = []

    if len(a) == 2 and len(b) == 2:
        result.append((a[0] * b[1]) - (a[1] * b[0]))
        return result[0]
    else:
        result.append((a[1] * b[2]) - (a[2] * b[1]))
        result.append((a[2] * b[0]) - (a[0] * b[2]))
        result.append((a[0] * b[1]) - (a[1] * b[0]))

    return result

# Operación punto entre 2 vectores
def dot(a, b):
    result = []
    dot_result = 0

    if isinstance(a, (float, int)):
        for i in range(len(b)):
            result.append(a * b[i])
        return result
    elif len(a) == len(b):
        for i in range(len(a)):
            result.append(a[i] * b[i])
        for r in result:
            dot_result += r
        return dot_result
    else:
        return


def hypotenuse(v):
    r = 0
    for a in v:
        r += pow(a, 2)

    r = pow(r, 0.5)

    return r


# Normaliza un vector
def normalize(v):
    result = []
    r = 0
    for a in v:
        r += pow(a, 2)

    r = pow(r, 0.5)

    if r != 0:
        for a in v:
            result.append(a / r)
    else:
        return v

    return result

# Valor aproximado de pi
def pi():
    return 3.1415926535897932384626433

# Convierte de grados a radianes
def deg2rad(deg):
    return (deg * pi()) / 180

class Matrix(object):
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

    def __len__(self):
        return len(self.matrix)

    # Multiplicación matrix * matrix o matrix * vector
    def __matmul__(self, other):

        # Valida si el segundo argumento es una matrix
        if isinstance(other, Matrix):
            c = Matrix([[0 for x in range(other.cols)] for y in range(self.rows)])

            if self.cols != other.rows:
                raise ValueError('The number of columns (first matrix), and rows (second matrix) must coincide')

            for y in range(self.rows):
                for a in range(other.cols):
                    x = 0
                    for b in range(other.rows):
                        x += self.matrix[y][b] * other.matrix[b][a]
                    c.matrix[y][a] = x

        # Valida si el segundo argumento es un vector
        # Arreglar validación para que verifique si es una instancia de V3 o V4
        else:
            c = Matrix([[0 for x in range(self.rows)] for y in range(1)])
            rows = len(other)
            if self.cols != rows:
                raise ValueError('The number of columns of the matrix, and the size of the vector must coincide')
            for y in range(self.rows):
                x = 0
                for a in range(rows):
                    x += self.matrix[y][a] * other[a]
                c.matrix[0][y] = x

        return c

    # Elimina una fila o columna de una matrix
    def delete(self, obj, axis=None):
        # Elimina una columna
        result = []
        if axis == 1:
            for y in self.matrix:
                fila = []
                for x in range(len(y)):
                    if x != obj:
                        fila.append(y[x])
                result.append(fila)
        # Elimina una fila
        else:
            cont = 0
            for fila in self.matrix:
                if cont != obj:
                    result.append(fila)
                cont += 1

        return result

    # Calcula  el determinante de una matrix
    def det(self):
        if self.cols != self.rows:
            raise ValueError('The number of columns and rows must coincide')

        determinant = 0
        # Verifica que la dimensión de la matriz sea mayor a 2
        if self.rows != 2:
            cols = []
            rows = []
            # Busca filas y columnas con 0
            for y in range(self.rows):
                fila = 0
                col = 0
                for x in range(self.cols):
                    if self.matrix[y][x] == 0:
                        fila += 1
                    if self.matrix[x][y] == 0:
                        col += 1
                rows.append(fila)
                cols.append(col)

            # Evalúa las filas y columnas para utilizar la que tiene más 0´s
            col = max(cols)
            row = max(rows)

            # Cuando hay más 0´s en las columnas
            if col > row:
                x = cols.index(col)
                determinant = 0
                for y in range(self.rows):
                    det = 0
                    if self.matrix[y][x] != 0:
                        matrix = Matrix(self.delete(x, 1))
                        a_matrix = Matrix(matrix.delete(y))
                        value = pow(-1, (y + x)) * self.matrix[y][x]
                        if a_matrix.rows == 3:
                            det = value * a_matrix.det()
                        if a_matrix.rows == 2:
                            adjunto = (a_matrix.matrix[0][0] * a_matrix.matrix[1][1]) - \
                                      (a_matrix.matrix[0][1] * a_matrix.matrix[1][0])
                            det = value * adjunto
                    determinant += det
            # Cuando hay más 0´s en las filas o tienen la misma cantidad de 0´s
            else:
                y = rows.index(row)
                determinant = 0
                for x in range(self.rows):
                    det = 0
                    if self.matrix[y][x] != 0:
                        matrix = Matrix(self.delete(x, 1))
                        a_matrix = Matrix(matrix.delete(y))
                        value = pow(-1, (y + x)) * self.matrix[y][x]
                        if a_matrix.rows == 3:
                            det = value * a_matrix.det()
                        if a_matrix.rows == 2:
                            adjunto = (a_matrix.matrix[0][0] * a_matrix.matrix[1][1]) - \
                                      (a_matrix.matrix[0][1] * a_matrix.matrix[1][0])
                            det = value * adjunto
                    determinant += det
        # Cuando la dimensión de la matriz es igual a 2
        elif self.rows == 2:
            determinant = (self.matrix[0][0] * self.matrix[1][1]) - \
                          (self.matrix[0][1] * self.matrix[1][0])

        return determinant

    # Encuentra la matriz adjunta
    def adjunctMatrix(self):
        result = Matrix([[0 for x in range(self.cols)] for y in range(self.rows)])

        for y in range(self.rows):
            for x in range(self.cols):
                matrix = Matrix(self.delete(x, 1))
                a_matrix = Matrix(matrix.delete(y))
                result.matrix[y][x] = pow(-1, (y + x)) * a_matrix.det()

        return result.matrix

    # Encuentra la matriz transpuesta
    def transpose(self):
        result = Matrix([[0 for x in range(self.cols)] for y in range(self.rows)])
        for y in range(self.rows):
            for x in range(self.cols):
                result.matrix[x][y] = self.matrix[y][x]
        return result

    # Encuentra la inversa de una matriz
    def inv(self):
        result = Matrix([[0 for x in range(self.cols)] for y in range(self.rows)])
        adj = self.transpose().adjunctMatrix()
        det = self.det()
        for y in range(self.rows):
            for x in range(self.cols):
                result.matrix[y][x] = adj[y][x] / det

        return result

