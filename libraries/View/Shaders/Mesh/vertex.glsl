#version 150

in vec3 a_position;
out vec3 pos_mv;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position, 1.0);
    pos_mv = (model_view_matrix * vec4(a_position, 1.0)).xyz;
}
