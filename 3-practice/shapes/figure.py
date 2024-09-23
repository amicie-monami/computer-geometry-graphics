from numpy import ndarray 
from shader import Shader
from OpenGL.GL import *
from .shape import Shape
import glm
import numpy as np

class Figure(Shape):

    def __init__(
            self, 
            draw_mood, 
            shader: Shader, 
            vertices: ndarray, 
            indices=None,
            size=1, 
            smooth_mode=None, 
            front_and_back_mode=None, 
            front_mode=None, 
            back_mode=None
        ):
        self.size = size  
        self.shader = shader
        self.draw_func = None
        self.draw_mood = draw_mood
        self.smooth_mode = smooth_mode
        self.transform_matrix = glm.mat4(1.0)

        super().__init__(vertices, indices, front_and_back_mode, front_mode, back_mode)
    
    def draw(self):
        if self.draw_mood == GL_LINES:
            glLineWidth(self.size)
        elif self.draw_mood == GL_POINTS:
            glPointSize(self.size)
        
        self.shader.use()
        self.__transform__()

        super().draw(self.draw_mood, self.smooth_mode)

        if self.draw_mood == GL_LINES:
            glLineWidth(1)
        elif self.draw_mood == GL_POINTS:
            glPointSize(1)

    def __transform__(self):
        transform_loc = glGetUniformLocation(self.shader.get_program(), "transform")
        if transform_loc == -1:
            return
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(self.transform_matrix))

    def transform(self, matrix):
        if type(matrix) == list:
            for mt in matrix:
                self.transform_matrix @= mt
            return        
        self.transform_matrix @= matrix

    def transform_reset(self):
        self.transform_matrix = glm.mat4(1.0)
