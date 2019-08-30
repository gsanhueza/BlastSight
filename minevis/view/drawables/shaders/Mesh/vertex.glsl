#version 140

in vec3 a_position;
in vec4 a_color;
in int a_wireframe;
out vec3 pos_mv;
out vec4 v_color;
flat out int v_wireframe;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position, 1.0);
    pos_mv = (model_view_matrix * vec4(a_position, 1.0)).xyz;
    v_color = a_color;
    v_wireframe = a_wireframe;
}
