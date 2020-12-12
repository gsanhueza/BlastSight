#version 330

layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
out vec2 TexCoords;

uniform mat4 model_view_matrix;
uniform mat4 proj_matrix;

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

    gl_Position = proj_matrix * modelView * vec4(vertex.xy, 0.0, 1.0);
    TexCoords = vertex.zw;
}
