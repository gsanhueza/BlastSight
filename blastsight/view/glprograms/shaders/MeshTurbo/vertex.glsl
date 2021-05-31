#version 140
#extension GL_ARB_explicit_attrib_location : require

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec4 a_color;

out vec3 pos_mv;
out vec4 v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec3 rendering_offset;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position + rendering_offset, 1.0);
    pos_mv = (model_view_matrix * vec4(a_position + rendering_offset, 1.0)).xyz;
    v_color = a_color;
}
