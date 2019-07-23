#version 140

in vec3 a_position;
in vec3 a_color;

out vec3 v_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    mat4 mvp = proj_matrix * model_view_matrix;

//    // The original matrix is this
//    mat4 only_rot = mat4(mvp[0][0], mvp[0][1], mvp[0][2], mvp[0][3],
//                         mvp[1][0], mvp[1][1], mvp[1][2], mvp[1][3],
//                         mvp[2][0], mvp[2][1], mvp[2][2], mvp[2][3],
//                         mvp[3][0], mvp[3][1], mvp[3][2], mvp[3][3]);

//    // This matrix allow us to rotate and scale lines, without translating them
    vec4 rot_vec = vec4(-12.0, -12.0, 0.0, 15.0);
    mat4 only_rot = mat4(mvp[0][0], mvp[0][1], mvp[0][2], mvp[0][3],
                         mvp[1][0], mvp[1][1], mvp[1][2], mvp[1][3],
                         mvp[2][0], mvp[2][1], mvp[2][2], mvp[2][3],
                         rot_vec);

//    gl_Position = mvp * vec4(a_position, 1.0);
    gl_Position = only_rot * vec4(a_position, 1.0);
    v_color = a_color;
}
