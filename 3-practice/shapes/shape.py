from OpenGL.GL import *

class Shape:
    
    def __init__(self, shader, vertices, indices, front_and_back_mode, front_mode, back_mode):
        self.shader = shader
        self.vertices = vertices
        self.indices = indices

        self.ebo = None
        self.vao = None
        self.vbo = None

        self.front_and_back_mode = front_and_back_mode
        self.front_mode = front_mode
        self.back_mode = back_mode
        
        self.vertices_count = len(self.vertices) // 6
        self.__init_buffers__()


    def draw(self, draw_mode, smooth_mode):
        """
        The proccess of rendering a shape on the screen
        """
        self.bind_polygon_mode()
        if smooth_mode is not None:
            glEnable(smooth_mode)

        self.render(draw_mode)

        glBindVertexArray(0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if smooth_mode is not None:
            glDisable(smooth_mode)
        

    def render(self, draw_mode):
        """
        Rendering
        """
        self.shader.use()
        glBindVertexArray(self.vao)
        if self.ebo is not None:
            glDrawElements(draw_mode, len(self.indices), GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(draw_mode, 0, self.vertices_count)


    def bind_polygon_mode(self):
        """
        Binding front and back layers modes
        """
        if self.front_and_back_mode is not None:
            glPolygonMode(GL_FRONT_AND_BACK, self.front_and_back_mode)
            return 
        
        if self.front_mode is not None:
            glPolygonMode(GL_FRONT, self.front_mode)

        if self.back_mode is not None:
            glPolygonMode(GL_BACK, self.back_mode) 


    def __init_buffers__(self):
        """
        Initializes and binds the Vertex Array Object (VAO), Vertex Buffer Object (VBO), Elements Buffer Object (EBO)
        This sets up the buffer memory and uploads vertex data to the GPU
        """
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        if self.indices is not None:
            self.ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        self.__set_attributes__()
        glBindVertexArray(0)



    def __set_attributes__(self):
        """
        Setting the vertex attributes(coordinates, color)
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
  