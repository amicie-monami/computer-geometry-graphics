import numpy
from .shader import Shader
from OpenGL.GL import *

class Point:

    def __init__(self, shader: Shader, pos: numpy.ndarray, color: numpy.ndarray, size, smooth=False):
        self.shader = shader
        self.pos = pos     #x y z
        self.color = color #r g b
        self.size = size   #size
        self.smooth = smooth
        self._set_attributes()
    
    def draw(self):
        """Drawing the point at the screen"""
        self.shader.use()
        glBindVertexArray(self.vao)
        glPointSize(self.size)

        if self.smooth:
            glEnable(GL_POINT_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glDrawArrays(GL_POINTS, 0, 1)

        if self.smooth:
            glDisable(GL_POINT_SMOOTH)

    def _set_attributes(self):
        """Set shape attributes"""
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        vertices = numpy.concatenate([self.pos, self.color])
        
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        #position
        attribute_idx = 0
        stride = 6 * 4
        glVertexAttribPointer(attribute_idx, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(attribute_idx)

        #color
        attribute_idx = 1
        offset_to_color = 3 * 4
        glVertexAttribPointer(attribute_idx, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset_to_color))
        glEnableVertexAttribArray(attribute_idx)
    