import numpy
from random import random as rand

def prepare_vertices(vertices_coords):
    vertices = []
    for x, y, z in vertices_coords:
        coords = [x, y, z]
        color = [rand() for _ in range(3)]
        vertices.extend(coords + color)        
    return numpy.array(vertices, dtype=numpy.float32)

def prepare_indices(indices):
    return numpy.array(indices, dtype=numpy.uint32)