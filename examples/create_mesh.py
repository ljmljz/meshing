import meshing

points = [0.0,0.0, 100.0,0.0, 100.0,100.0, 0.0,100.0]
polygon = meshing.Polygon()

for i in range(0, len(points), 2):
    start = points[i: i + 2]
    end = points[i + 2: i + 4] if i + 4 < len(points) else points[:2]

    line = meshing.Line(start, end)
    polygon.append(line)

mesh = meshing.Mesh()
mesh.extrude(polygon, 10)
mesh.update_normals()

print mesh.vertices
print mesh.faces
print mesh.normals
