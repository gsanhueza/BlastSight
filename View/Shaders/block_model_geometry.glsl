#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout (points) in;
layout (line_strip, max_vertices = 2) out;

layout (location = 1) in vec3 v_color[1];
layout (location = 1) out vec3 f_color;

uniform float voxSize = 5.0;
uniform mat4 mvp = proj_matrix * model_view_matrix;

void AddQuad(vec4 center, vec4 dy, vec4 dx)
{
    f_color = v_color[0];
    gl_Position = center + (dx - dy);
    EmitVertex();

    f_color = v_color[0];
    gl_Position = center + (-dx - dy);
    EmitVertex();

    f_color = v_color[0];
    gl_Position = center + (dx + dy);
    EmitVertex();

    f_color = v_color[0];
    gl_Position = center + (-dx + dy);
    EmitVertex();

    EndPrimitive();
}

void main()
{
    vec4 center = gl_in[0].gl_Position;

    vec4 dx = mvp[0] / 2.0f * voxSize;
    vec4 dy = mvp[1] / 2.0f * voxSize;
    vec4 dz = mvp[2] / 2.0f * voxSize;

//    AddQuad(center + dx, dy, dz);
//    AddQuad(center - dx, dz, dy);
//    AddQuad(center + dy, dz, dx);
//    AddQuad(center - dy, dx, dz);
//    AddQuad(center + dz, dx, dy);
//    AddQuad(center - dz, dy, dx);

    gl_Position = gl_in[0].gl_Position + vec4(1.0, 0.0, 0.0, 1.0);
    f_color = v_color[0];

    EmitVertex();

    gl_Position = gl_in[0].gl_Position + vec4(-1.0, 0.0, 0.0, 1.0);
    f_color = v_color[0];

    EmitVertex();

    EndPrimitive();
}
