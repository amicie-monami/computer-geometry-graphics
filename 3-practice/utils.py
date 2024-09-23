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

def prepare_vertices(vertices_coords):
    vertices = []
    for x, y, z in vertices_coords:
        coords = [x, y, z]
        color = [rand() for _ in range(3)]
        vertices.extend(coords + color)        
    return numpy.array(vertices, dtype=numpy.float32)

def scale_matrix(sx, sy, sz):
    return numpy.array([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1],
    ], dtype=numpy.float32)

def rotation_matrix_z(angle):
    cos_theta = numpy.cos(angle)
    sin_theta = numpy.sin(angle)
    return numpy.array([
        [cos_theta, -sin_theta, 0, 0],
        [sin_theta, cos_theta,  0, 0],
        [0,         0,          1, 0],
        [0,         0,          0, 1],
    ], dtype=numpy.float32)

def translation_matrix(tx, ty, tz):
    return numpy.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1],
    ], dtype=numpy.float32)