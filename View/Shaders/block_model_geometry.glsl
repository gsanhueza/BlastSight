#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

layout (location = 1) in vec3 v_color[1];
layout (location = 1) out vec3 f_color;

uniform float voxSize = 5.0;
uniform mat4 mvp = proj_matrix * model_view_matrix;

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

void build_house(vec4 position)
{
    gl_Position = position + vec4(-0.2, -0.2, 0.0, 0.0);    // 1:bottom-left
    f_color = v_color[0];
    EmitVertex();

    gl_Position = position + vec4( 0.2, -0.2, 0.0, 0.0);    // 2:bottom-right
    f_color = v_color[0];
    EmitVertex();

    gl_Position = position + vec4(-0.2,  0.2, 0.0, 0.0);    // 3:top-left
    f_color = v_color[0];
    EmitVertex();

    gl_Position = position + vec4( 0.2,  0.2, 0.0, 0.0);    // 4:top-right
    f_color = v_color[0];
    EmitVertex();

    EndPrimitive();
}

void main()
{
    vec4 dx = mvp[0] / 2.0f * voxSize;
    vec4 dy = mvp[1] / 2.0f * voxSize;
    vec4 dz = mvp[2] / 2.0f * voxSize;

    vec4 center = gl_in[0].gl_Position;
//    AddQuad(center + dx, dy, dz);
    build_house(center);
}
