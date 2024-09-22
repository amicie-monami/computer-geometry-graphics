import numpy as np
from shader import Shader
from OpenGL.GL import *
from .shape import Shape

class Figure(Shape):

    def __init__(
            self, 
            draw_mood, 
            shader: Shader, 
            vertices: np.ndarray, 
            indices=None,
            size=1, 
            smooth_mode=None, 
            front_and_back_mode=None, 
            front_mode=None, 
            back_mode=None
        ):
        
        self.size = size  
        self.draw_mood = draw_mood
        self.smooth_mode = smooth_mode
        super().__init__(shader, vertices, indices, front_and_back_mode, front_mode, back_mode)
    
    def draw(self):
        if self.draw_mood == GL_LINES:
            glLineWidth(self.size)
        elif self.draw_mood == GL_POINTS:
            glPointSize(self.size)
            
        super().draw(self.draw_mood, self.smooth_mode)

        if self.draw_mood == GL_LINES:
            glLineWidth(1)
        elif self.draw_mood == GL_POINTS:
            glPointSize(1)

        
        
