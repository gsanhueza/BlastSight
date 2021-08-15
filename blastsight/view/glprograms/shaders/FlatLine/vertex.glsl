#version 140
#extension GL_ARB_explicit_attrib_location : require

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec4 a_color;

out vec4 v_color;

void main()
{
    // The flat line uses NDC coordinates directly => Matrices are not required at all
    gl_Position = vec4(a_position, 1.0);
    v_color = a_color;
}
