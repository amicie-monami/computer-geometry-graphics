import numpy as np
from shader import Shader
from OpenGL.GL import *
from .shape import Shape

class Point(Shape):

    def __init__(self, shader: Shader, pos: np.ndarray, color: np.ndarray, size: float, smooth=False):
        self.size = size
        vertices = np.concatenate([pos, color]) 
        super().__init__(shader, vertices, smooth)
    
    def draw(self):
        glPointSize(self.size)
        super().draw(GL_POINTS, GL_POINT_SMOOTH, 1)
