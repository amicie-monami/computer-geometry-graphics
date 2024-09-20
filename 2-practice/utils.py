import numpy

def calculate_polygon_vertices(n, scale_x=1.0, scale_y=1.0):
    vertices = []
    angle_offset = numpy.pi / 2  
    for i in range(n):
        angle = 2 * numpy.pi * i / n + angle_offset  
        x = numpy.cos(angle) * scale_x
        y = numpy.sin(angle) * scale_y
        vertices.append((x, y))
    return vertices

