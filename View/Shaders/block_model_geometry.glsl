#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout (points) in;
layout (triangle_strip, max_vertices = 24) out;

layout (location = 1) in vec3 v_color[1];
layout (location = 1) out vec3 f_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec2 block_size;

mat4 mvp = proj_matrix * model_view_matrix;

void AddQuad(vec4 center, vec4 dy, vec4 dx)
{
    gl_Position = center + (dx - dy);
    f_color = v_color[0];
    EmitVertex();

    gl_Position = center + (-dx - dy);
    f_color = v_color[0];
    EmitVertex();

    gl_Position = center + (dx + dy);
    f_color = v_color[0];
    EmitVertex();

    gl_Position = center + (-dx + dy);
    f_color = v_color[0];
    EmitVertex();

    EndPrimitive();
}

void main()
{
    // FIXME This can be made with half the vertices (Hint: Visibility)
    vec4 center = gl_in[0].gl_Position;

    vec4 dx = mvp[0] / 2.0f * block_size.x;
    vec4 dy = mvp[1] / 2.0f * block_size.x;
    vec4 dz = mvp[2] / 2.0f * block_size.x;

    AddQuad(center + dx, dy, dz);  // Right
    AddQuad(center - dx, dz, dy);  // Left
    AddQuad(center + dy, dz, dx);  // Top
    AddQuad(center - dy, dx, dz);  // Bottom
    AddQuad(center + dz, dx, dy);  // Front
    AddQuad(center - dz, dy, dx);  // Back
}
