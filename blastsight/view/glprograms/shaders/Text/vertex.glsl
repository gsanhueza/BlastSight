#version 330

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;
layout (location = 2) in vec2 a_texcoords;

out vec3 v_color;
out vec2 v_texcoords;

uniform mat4 model_view_matrix;
uniform mat4 proj_matrix;
uniform vec3 rendering_offset;

mat4 billboard_matrix(mat4 matrix)
{
    // First column.
    matrix[0][0] = 1.0;
    matrix[0][1] = 0.0;
    matrix[0][2] = 0.0;

    // Second column.
    matrix[1][0] = 0.0;
    matrix[1][1] = 1.0;
    matrix[1][2] = 0.0;

    // Third column.
    matrix[2][0] = 0.0;
    matrix[2][1] = 0.0;
    matrix[2][2] = 1.0;

    return matrix;
}

void main()
{
    // Billboard model_view_matrix
    mat4 modelView = model_view_matrix;
//    mat4 modelView = billboard_matrix(model_view_matrix);

    gl_Position = proj_matrix * modelView * vec4(a_position + rendering_offset, 1.0);
    v_color = a_color;
    v_texcoords = a_texcoords;
}
