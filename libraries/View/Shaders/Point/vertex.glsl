#version 140

attribute vec3 a_position;
attribute float a_color;

varying float v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform float point_size;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position, 1.0);
    gl_PointSize = point_size;
    v_color = a_color;
}
