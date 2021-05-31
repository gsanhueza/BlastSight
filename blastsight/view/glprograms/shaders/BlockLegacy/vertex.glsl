#version 140
#extension GL_ARB_explicit_attrib_location : require

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;
layout (location = 2) in float a_alpha;
layout (location = 3) in vec3 a_template;

out vec3 pos_mv;
out vec3 v_color;
out float v_alpha;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec3 rendering_offset;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position + a_template + rendering_offset, 1.0);
    pos_mv = (model_view_matrix * vec4(a_position + a_template + rendering_offset, 1.0)).xyz;
    v_color = a_color;
    v_alpha = a_alpha;
}
