import os
import json
import logging
import math
import copy
import numpy

import geometry as geo


class BaseShape(object):
    def __init__(self):
        self._points = None

    @property
    def points(self):
        return self._points

    def deg2rad(deg):
        return round((deg * math.pi / 180.0), 2)

    def translate(self, offset=None):
        if not offset:
            return

        if isinstance(offset, (list, tuple)):
            self._points = (self._points.reshape(-1, 2) * numpy.array(offset)).reshape(-1)
        else:
            raise

    def rotate(self, angle):
        pass

    def mirror(self):
        pass

    def scale(self, rate):
        self._vertices = map(lambda x: round(x * rate, 2), self._vertices)


class Line(BaseShape):
    def __init__(self, start, end, width=0):
        super(BaseShape, self).__init__()

        assert isinstance(start, (list, tuple))
        assert isinstance(end, (list, tuple))

        self.start = start
        self.end = end
        self.width = width

        self._points = numpy.array([start, end])


class Arc(BaseShape):
    def __init__(self, start, end, center, radius=0, cw=True, width=0.0):
        super(Arc, self).__init__()

        assert isinstance(start, (list, tuple))
        assert isinstance(end, (list, tuple))
        assert isinstance(center, (list, tuple))

        self.start = start
        self.end = end
        self.center = center
        self.radius = radius
        self.cw = cw
        self._precision = 6
        self.width = width

        self._calc_points()

    def _calc_points(self):
        if self._radius <= 0:
            self._calc_radius()

        is_circle = False
        if self.start[0] == self.end[0] and self.start[1] == self.end[1]:
            is_circle = True

        start_angle = math.atan2(
            self.start[1] - self.center[1],
            self.start[0] - self.center[0]
        )

        if is_circle:
            end_angle = 2 * math.pi + start_angle
        else:
            end_angle = math.atan2(
                self.end[1] - self.center[1],
                self.end[0] - self.center[0]
            )

        precision = self._precision if abs(end_angle - start_angle) < math.pi else self._precision * 2
        prefix = -1 if self.cw else 1
        step_angle = abs(end_angle - start_angle) / precision
        points = list(self.start)

        for n in range(1, precision):
            x = round(self.center[0] + self._radius * math.cos(start_angle + prefix * n * step_angle), 2)
            y = round(self.center[1] + self._radius * math.sin(start_angle + prefix * n * step_angle), 2)
            points.extend([x, y])

        points.extend(self.end)
        self._points = numpy.array(points)

    def _calc_radius(self):
        self._radius = round(
            math.sqrt(
                (self.center[0] - self.start[0]) * (self.center[0] - self.start[0])
                + (self.center[1] - self.start[1]) * (self.center[1] - self.start[1])
            ),
            2
        )


class Polygon(BaseShape):
    def __init__(self):
        super(Polygon, self).__init__()
        self._holes = []
        self._shapes = []

    def append(self, shape):
        assert isinstance(shape, (Line, Arc))

        self._shapes.append(shape)

    def add_hole(self, hole):
        assert isinstance(hole, Hole)

        self._holes.append(hole)

    @property
    def holes(self):
        return self._holes

    @property
    def points(self):
        if self._points:
            return self._points

        for shape in self._shapes:
            if not self._points:
                self._points = [shape.points]
            else:
                if cmp(self._points[0][-2:], shape.points[:2]) == 0:
                    if cmp(self._points[0][:2], shape.points[-2:]) != 0:
                        self._points[0].append(shape.points[2:])
                else:
                    self._points[0].append(shape.points)

        for hole in self._holes:
            self._points.append(hole.points)

        return self._points


class Hole(BaseShape):
    def __init__(self):
        super(Hole, self).__init__()
        self._shapes = []

    def append(self, shape):
        assert isinstance(shape, (Line, Arc))

        self._shapes.append(shape)

    @property
    def points(self):
        if self._points:
            return self._points

        for shape in self._shapes:
            if not self._points:
                self._points = shape.points
            else:
                if cmp(self._points[-2:], shape.points[:2]) == 0:
                    if cmp(self._points[:2], shape.points[-2:]) != 0:
                        self._points.append(shape.points[2:])
                else:
                    self._points.append(shape.points)

        return self._points


class Rectangle(Polygon):
    def __init__(self, start, end):
        super(Rectangle, self).__init__()

        assert isinstance(start, (list, tuple))
        assert isinstance(end, (list, tuple))

        self.start = start
        self.end = end

    def _calc_points(self):
        if len(self.start) <= 0 or len(self.end) <= 0:
            return

        # CounterClockwise
        self._shapes.append(Line([self.start[0], self.start[1]], [self.start[0], self.end[1]]))
        self._shapes.append(Line([self.start[0], self.end[1]], [self.end[0], self.end[1]]))
        self._shapes.append(Line([self.end[0], self.end[1]], [self.end[0], self.start[1]]))
        self._shapes.append(Line([self.end[0], self.start[1]], [self.start[0], self.start[1]]))




#if __name__ == "__main__":
