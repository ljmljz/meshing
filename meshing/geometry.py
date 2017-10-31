import _geometry as geo


class Geometry(object):
    instance = None

    def __init__(self, points=None):
        if points and isinstance(points, list):
            self.instance = geo.Geometry(points)
        else:
            self.instance = geo.Geometry()

        self.triangles = None

    @property
    def polygon(self):
        return self.instance.polygon

    @polygon.setter
    def polygon(self, v):
        if isinstance(v, list):
            self.instance.polygon(v)
        else:
            raise

    @property
    def vertices(self):
        return self.instance.vertices

    @property
    def faces(self):
        return self.instance.faces

    def triangulate(self):
        self.triangles = self.instance.triangulate()
        return self.triangles

    def extrude(self, v):
        if not isinstance(v, int):
            raise

        if not self.triangles:
            self.triangulate()

        return self.instance.extrude(v)