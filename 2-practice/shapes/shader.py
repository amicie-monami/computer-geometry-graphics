from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import atexit

class Shader:

    def __init__(self, vertex_filepath: str, fragment_filepath: str):
        self._create_shader_program(vertex_filepath, fragment_filepath)
        atexit.register(self._cleanup)
    
    def use(self):
        """Activate shader"""
        glUseProgram(self.program)

    def _create_shader_program(self, vertex_filepath, fragment_filepath):
        """Create shader program with vertex and fragment shaders"""
        vertex   = self._create_shader_module(vertex_filepath, GL_VERTEX_SHADER)
        fragment = self._create_shader_module(fragment_filepath, GL_FRAGMENT_SHADER)

        self.program = shaders.compileProgram(vertex, fragment)

        glDeleteShader(vertex)
        glDeleteShader(fragment)

    def _create_shader_module(self, filepath: str, module_type: int) -> int:
        """Read shader's code from file"""
        with open(filepath, "r") as file:
            source_code = file.read()
        return shaders.compileShader(source_code, module_type)

    def _cleanup(self):
        """Delete a created program"""
        glDeleteProgram(self.program)
