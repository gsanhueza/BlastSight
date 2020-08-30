#version 140
#extension GL_ARB_explicit_attrib_location : require

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;

out vec3 v_color;

uniform mat4 model_view_matrix;

void main()
{
    mat4 mv = model_view_matrix;
    // This matrix allow us to rotate, without translating (bottom row) or scaling (rightmost column)
    mat4 rot_mat = mat4(mv[0][0], mv[0][1], mv[0][2], 0.0,
                        mv[1][0], mv[1][1], mv[1][2], 0.0,
                        mv[2][0], mv[2][1], mv[2][2], 0.0,
                        0.0, 0.0, 0.0, 1.0);

    gl_Position = rot_mat * vec4(a_position, 1.0);
    v_color = a_color;
}
