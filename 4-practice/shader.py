from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import atexit

class Shader:

    def __init__(self, vertex_filepath, fragment_filepath):
        self.__create_shader_program__(vertex_filepath, fragment_filepath)
        atexit.register(self.__cleanup__)
    
    def use(self):
        glUseProgram(self.program)

    def get_program(self):
        return self.program

    def __create_shader_program__(self, vertex_filepath, fragment_filepath):
        vertex   = self.__create_shader_module__(vertex_filepath, GL_VERTEX_SHADER)
        fragment = self.__create_shader_module__(fragment_filepath, GL_FRAGMENT_SHADER)
        self.program = shaders.compileProgram(vertex, fragment)
        glDeleteShader(vertex)
        glDeleteShader(fragment)

    def __create_shader_module__(self, filepath, module_type):
        with open(filepath, "r") as file:
            source_code = file.read()
        return shaders.compileShader(source_code, module_type)

    def __cleanup__(self):
        glDeleteProgram(self.program)
