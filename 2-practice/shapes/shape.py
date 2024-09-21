from OpenGL.GL import *

class Shape:
    
    def __init__(self, shader, vertices, smooth):
        self.shader = shader
        self.vertices = vertices
        self.smooth = smooth
        self.vao = None
        self.vbo = None
        self.__init_buffers__()
        self.__set_attributes__()

    def draw(self, draw_mode, smooth_mode, vertex_count):
        """
        Rendering the shape on the screen.
        """
        if self.smooth:
            glEnable(smooth_mode)

        self.shader.use()
        glBindVertexArray(self.vao)
        glDrawArrays(draw_mode, 0, vertex_count)

        if self.smooth:
            glDisable(smooth_mode)


    def __init_buffers__(self):
        """
        Initializes and binds the Vertex Array Object (VAO) and Vertex Buffer Object (VBO).
        This sets up the buffer memory and uploads vertex data to the GPU.
        """
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

    def __set_attributes__(self):
        """
        Setting the shape attributes: (position, color)
        """
        #(layout(location = 0))
        position_attribute_idx = 0
        position_size = 3  #x,y,z
        stride = 6 * 4     #len([x,y,z,r,g,b])*sizeof(float32)
        glVertexAttribPointer(position_attribute_idx, position_size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position_attribute_idx)

        #(layout(location = 1))
        color_attribute_idx = 1
        color_size = 3  #r,g,b 
        offset_to_color = 3 * 4  #skip xyz - offset to rgb
        glVertexAttribPointer(color_attribute_idx, color_size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset_to_color))
        glEnableVertexAttribArray(color_attribute_idx)
