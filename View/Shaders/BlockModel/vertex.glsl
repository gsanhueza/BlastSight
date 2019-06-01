#version 150
#extension GL_ARB_separate_shader_objects : enable

in vec3 a_position;
in vec3 a_color;

out vec3 v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position, 1.0);
    gl_PointSize = clamp(20.0 / gl_Position.z, 2.0, 10.0);
    v_color = a_color;
}
