import numpy
from random import random as rand

def calculate_polygon_vertices(n, scale_x=1.0, scale_y=1.0):
    vertices = []
    angle_offset = numpy.pi / 2  
    for i in range(n):
        angle = 2 * numpy.pi * i / n + angle_offset  
        x = numpy.cos(angle) * scale_x
        y = numpy.sin(angle) * scale_y
        vertices.append((x, y, 1.0))
    return vertices

2 * 180 * 0 / 3 + 90
2 * 180 * 1 / 3 + 90
2 * 180 * 2 / 3 + 90
 
360 / 3 + 90

def prepare_vertices(vertices_coords):
    vertices = []
    for x, y, z in vertices_coords:
        coords = [x, y, z]
        color = [rand() for _ in range(3)]
        vertices.extend(coords + color)        
    return numpy.array(vertices, dtype=numpy.float32)