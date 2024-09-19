from OpenGL.GL import *
import OpenGL.GL.shaders as shaders

def create_shader_program(vertex_filepath: str, fragment_filepath: str) -> int:
    vertex_module = create_shader_module(vertex_filepath, GL_VERTEX_SHADER)
    fragment_module = create_shader_module(fragment_filepath, GL_FRAGMENT_SHADER)

    shader_program = shaders.compileProgram(vertex_module, fragment_module)

    glDeleteShader(vertex_module)
    glDeleteShader(fragment_module)
    
    return shader_program

def create_shader_module(filepath: str, module_type: int) -> int:
    with open(filepath, "r") as file:
        source_code = file.read()
    return shaders.compileShader(source_code, module_type)
