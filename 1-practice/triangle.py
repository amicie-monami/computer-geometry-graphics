import numpy as np
from shaders import create_shader_program 
from OpenGL.GL import *
import atexit

class Triangle:
    def __init__(self, vertices: np.ndarray,  vertex_filepath: str, fragment_filepath: str):
        self.shader = create_shader_program(vertex_filepath, fragment_filepath)

        #generate vertex array
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        #generate position buffer
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        #attribute 0s: position
        attribute_index = 0
        size = 3
        stride = 3 * 4
        glVertexAttribPointer(attribute_index, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset=0))
        glEnableVertexAttribArray(0)

        #disable vao binding to avoid accidental modification
        glBindVertexArray(0)

        atexit.register(self.cleanup)

    def draw(self):
        glUseProgram(self.shader)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)
    
    def cleanup(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])

