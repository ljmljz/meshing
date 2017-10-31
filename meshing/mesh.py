import geometry
import shape
import numpy

ASCII_MODE = 1
BIN_MODE = 2


class Mesh(object):
    def __init__(self):
        self.vertices = None
        self.faces = None
        self.vectors = None
        self.normals = []
        self.texcoords = None
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
        self.vectors = vectors

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

    def rotate(self):
        pass


if __name__ == "__main__":
    polygon = [[0.0, 0.0, 100.0, 0.0, 100.0, 100.0, 0.0, 100.0]]
    m = Mesh()
    #m.extrude(polygon, 10)
    m.update_normals()