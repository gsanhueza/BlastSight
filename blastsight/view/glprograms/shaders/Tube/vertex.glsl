#version 140
#extension GL_ARB_explicit_attrib_location : require

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec4 a_color;
layout (location = 2) in vec2 a_properties;

out vec4 v_color;
out vec4 v_position;
out vec2 v_properties;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec3 rendering_offset;

void main()
{
    v_position = vec4(a_position + rendering_offset, 1.0);
    v_color = a_color;
    v_properties = a_properties;
}
