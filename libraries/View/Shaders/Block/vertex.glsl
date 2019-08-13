#version 140

in vec3 a_position;
in vec3 a_template;
in float a_color;

out vec3 pos_mv;
out float v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position + a_template, 1.0);
    pos_mv = (model_view_matrix * vec4(a_position + a_template, 1.0)).xyz;
    v_color = a_color;
}
