import numpy as np
from shader import Shader
from OpenGL.GL import *
from .shape import Shape

class Polygon(Shape):
    
    def __init__(self, shader: Shader, vertices_coords: np.ndarray, vertices_colors: np.ndarray, thickness: float, smooth=False):
        self.size = thickness  
        vertices = np.column_stack((vertices_coords.reshape(-1, 3), vertices_colors.reshape(-1, 3))).flatten()
        super().__init__(shader, vertices, smooth)
    
    def draw(self):
        glLineWidth(self.size)
        super().draw(GL_LINE_LOOP, GL_LINE_SMOOTH, len(self.vertices) // 6)
