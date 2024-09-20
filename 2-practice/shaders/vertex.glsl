#version 400 core

layout(location = 0) in vec3 position; // position attribute
layout(location = 1) in vec3 color;    // color attribute
layout(location = 2) in float size;    // size attribute

out vec3 fragColor;  

void main() {
    gl_Position = vec4(position, 1.0); // vec3(x y z) + a  
    fragColor = color;  // send data to a fragment shader
    gl_PointSize = size;  // point size
}
