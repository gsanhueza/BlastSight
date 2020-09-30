#version 140
#extension GL_ARB_explicit_attrib_location : require

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec4 a_color;

out vec3 v_position;
out vec4 v_color;

void main()
{
    v_position = a_position;
    v_color = a_color;
}
