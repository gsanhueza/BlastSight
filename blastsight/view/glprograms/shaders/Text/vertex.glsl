#version 330

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;
layout (location = 2) in vec2 a_texcoords;
layout (location = 3) in vec3 a_origin;

out vec3 v_color;
out vec2 v_texcoords;

uniform mat4 model_view_matrix;
uniform mat4 proj_matrix;
uniform vec3 rendering_offset;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(rendering_offset + a_origin + a_position , 1.0);
    v_color = a_color;
    v_texcoords = a_texcoords;
}
