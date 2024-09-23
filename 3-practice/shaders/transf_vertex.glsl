#version 400
layout(location = 0) in vec3 vertex_position;  
layout(location = 1) in vec3 vertex_color;     

uniform mat4 transform;

out vec3 fragColor;

void main ()
{
    gl_Position = transform * vec4 (vertex_position, 1.0);
    fragColor = vertex_color;
}