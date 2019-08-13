#version 140

in vec3 a_position;
in vec3 a_color;
in float point_size;
out vec3 v_color;

uniform vec2 viewport;
uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position, 1.0);
    v_color = a_color;
    gl_PointSize = viewport.y * point_size / (5 * gl_Position.w);
}
