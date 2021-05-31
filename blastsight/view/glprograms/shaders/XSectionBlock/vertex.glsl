#version 330

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;
layout (location = 2) in float a_alpha;

out vec3 v_position;
out vec3 v_color;
out float v_alpha;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    v_position = a_position;
    v_color = a_color;
    v_alpha = a_alpha;
}
