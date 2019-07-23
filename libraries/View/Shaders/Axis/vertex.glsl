#version 140

in vec3 a_position;
in vec3 a_color;

out vec3 v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    mat4 mvp = proj_matrix * model_view_matrix;
    // This matrix allow us to rotate, without translating (bottom row) or scaling (rightmost column)
    vec4 rot_vec = vec4(-12.0, -12.0, 0.0, 15.0);
    mat4 rot_mat = mat4(mvp[0][0], mvp[0][1], mvp[0][2], 0,
                        mvp[1][0], mvp[1][1], mvp[1][2], 0,
                        mvp[2][0], mvp[2][1], mvp[2][2], 0,
                        rot_vec);

    gl_Position = rot_mat * vec4(a_position, 1.0);
    v_color = a_color;
}
