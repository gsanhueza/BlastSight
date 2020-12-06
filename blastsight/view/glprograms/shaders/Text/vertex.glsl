#version 330

layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
out vec2 TexCoords;

uniform mat4 model_view_matrix;
uniform mat4 proj_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(vertex.xy, 0.0, 1.0);
    TexCoords = vertex.zw;
}
