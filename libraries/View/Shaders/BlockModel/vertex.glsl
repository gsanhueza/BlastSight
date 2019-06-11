#version 150

in vec3 a_position;
in vec3 a_color;
in vec3 a_template;

out vec3 pos_mv;
out vec3 v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position + a_template, 1.0);
    v_color = a_color;
//    pos_mv = (model_view_matrix * vec4(a_position + a_template, 1.0)).xyz;
}
