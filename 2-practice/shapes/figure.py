import numpy as np
from shader import Shader
from OpenGL.GL import *
from .shape import Shape

class Figure(Shape):

    def __init__(
            self, 
            shader: Shader, 
            vertices: np.ndarray, 
            draw_mood, 
            size=None, 
            smooth_mode=None, 
            front_and_back_mode=None, 
            front_mode=None, 
            back_mode=None
        ):
        
        self.size = size  
        self.draw_mood = draw_mood
        self.smooth_mode = smooth_mode
        super().__init__(shader, vertices, front_and_back_mode, front_mode, back_mode)
    
    def draw(self):
        if self.draw_mood == GL_LINES:
            glLineWidth(self.size)
        elif self.draw_mood == GL_POINTS:
            glPointSize(self.size)
            
        super().draw(self.draw_mood, self.smooth_mode, len(self.vertices) // 6)

        if self.draw_mood == GL_LINES:
            glLineWidth(1)
        elif self.draw_mood == GL_POINTS:
            glPointSize(1)

        
        
