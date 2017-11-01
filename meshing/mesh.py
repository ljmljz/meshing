from __future__ import print_function
import geometry
import shape
import numpy
import math
import datetime

from . import __title__, __version__, __url__

ASCII_MODE = 1
BIN_MODE = 2


class Mesh(object):
    def __init__(self):
        self.vertices = None
        self.faces = None
        # matrix 4 for calculating translation, rotation etc.
        self.vectors = None
        self.normals = []
        self.texcoords = []
        self.mode = ASCII_MODE

    def triangulate(self, polygon):
        assert isinstance(polygon, shape.Polygon)

        geo = geometry.Geometry(polygon.points)
        return geo.triangulate()

    def extrude(self, polygon, value):
        assert isinstance(polygon, shape.Polygon)
        assert isinstance(value, (int, float))

        geo = geometry.Geometry(polygon.points)
        self.faces = geo.extrude(value)
        self.vertices = geo.vertices

        vectors = numpy.array([])
        for face in self.faces:
            vectors = numpy.append(vectors, [self.vertices[face[0]], self.vertices[face[1]], self.vertices[face[2]]])

        vectors = vectors.reshape(-1, 3, 3)
        self.vectors = numpy.ones((len(vectors), 3, 4))
        self.vectors[:, :, :-1] = vectors

    def update_normals(self):
        v0 = self.vectors[:, 0, :3]
        v1 = self.vectors[:, 1, :3]
        v2 = self.vectors[:, 2, :3]

        normals = numpy.cross(v1 - v0, v2 - v0)

        for i in range(len(normals)):
            norm = numpy.linalg.norm(normals)
            if norm != 0:
                normals[i] /= numpy.linalg.norm(normals[i])

        self.normals[:] = normals

    def translate(self, tx=0, ty=0, tz=0):
        matrix = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [tx, ty, tz, 1]
        ], dtype=numpy.float32)
        self.vectors = self.vectors.dot(matrix)

        return self

    def scale(self, sx=1, sy=1, sz=1):
        matrix = numpy.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ], dtype=numpy.float32)
        self.vectors = self.vectors.dot(matrix)

    def rotate_x(self, degree):
        rad = math.radians(degree)
        matrix = numpy.array([
            [1, 0, 0, 0]
            [0, math.cos(rad), math.sin(rad), 0],
            [0, -math.sin(rad), math.cos(rad), 0],
            [0, 0, 0, 1]
        ], dtype=numpy.float32)
        self.vectors = self.vectors.dot(matrix)

        return self

    def rotate_y(self, degree):
        rad = math.radians(degree)
        matrix = numpy.array([
            [math.cos(rad), 0, -math.sin(rad), 0]
            [0, 1, 0, 0],
            [math.sin(rad), 0, math.cos(rad), 0],
            [0, 0, 0, 1]
        ], dtype=numpy.float32)
        self.vectors = self.vectors.dot(matrix)

        return self

    def rotate_z(self, degree):
        rad = math.radians(degree)
        matrix = numpy.array([
            [math.cos(rad), math.sin(rad), 0, 0]
            [-math.sin(rad), math.cos(rad), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=numpy.float32)
        self.vectors = self.vectors.dot(matrix)

        return self

    def save(self, filename, format='OBJ', mode=ASCII_MODE):
        pass

    def _save_obj(self, filename):
        vertices = numpy.zeros((len(self.vertices), 3), dtype=numpy.float32)
        for i, face in enumerate(self.faces):
            for j in range(3):
                vertices[face[0]][j] = self.vectors[i][j][:-1]

        with open(filename, "wb") as fh:
            print("# {} {}".format(__title__, __version__), file=fh)
            print("# {}".format(datetime.datetime.now()), file=fh)
            print("# {}".format(__url__), file=fh)
            print("", file=fh)
            for v in vertices:
                print("v {} {} {}".format(v[0], v[1], v[2]), file=fh)
                for vn in self.normals:
                    print("vn {} {} {}".format(vn[0], vn[1], vn[2]), file=fh)
                    for vt in self.texcoords:
                        print("vt {} {}".format(vt[0], vt[1]), file=fh)
                        for i, face in enumerate(self.faces):
                            print("f {}/{}/{} {}/{}/{} {}/{}/{}".format(
                                face[0] + 1, 3 * i + 1, i + 1,
                                face[1] + 1, 3 * i + 2, i + 1,
                                face[2] + 1, 3 * i + 3, i + 1,
                            ), file=fh)

    def _save_ascii_stl(self, filename):
        pass

    def _save_bin_stl(self, filename):
        pass

    def load(self, filename):
        pass