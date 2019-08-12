#version 150
#extension GL_ARB_separate_shader_objects : enable

in vec3 a_position;
in float a_color;

out float v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position, 1.0);
    v_color = a_color;
}
