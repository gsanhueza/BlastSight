#version 120

attribute vec3 a_position;
attribute float a_color;
attribute vec3 a_template;

varying vec3 pos_mv;
varying float v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position + a_template, 1.0);
    pos_mv = (model_view_matrix * vec4(a_position + a_template, 1.0)).xyz;
    v_color = a_color;
}
