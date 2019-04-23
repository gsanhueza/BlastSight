#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout (points) in;
layout (triangle_strip, max_vertices = 24) out;

layout (location = 1) in vec3 v_color[1];
layout (location = 1) out vec3 f_color;

layout (location = 2) out vec3 normal;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec2 block_size;

mat4 mvp = proj_matrix * model_view_matrix;

vec3 calculateNormal(vec4 v1, vec4 v2, vec4 v3)
{
    vec3 a = (v2 - v1).xyz;
    vec3 b = (v3 - v1).xyz;
    vec3 N = normalize(cross(b, a));

    // We're cheating here, but it's a simple way to ensure every normal aims outside (or every normal aims inside)
    if (length(N + v1.xyz) > length(v1.xyz))
    {
        N = -N;
    }

    return N;
}

void AddQuad(vec4 center, vec4 dy, vec4 dx)
{
    vec4 v1 = center + (dx - dy);
    vec4 v2 = center + (-dx - dy);
    vec4 v3 = center + (dx + dy);
    vec4 v4 = center + (-dx + dy);

    vec3 N = calculateNormal(v1, v2, v3);

    gl_Position = v1;
    f_color = v_color[0];
    normal = N;
    EmitVertex();

    gl_Position = v2;
    f_color = v_color[0];
    normal = N;
    EmitVertex();

    gl_Position = v3;
    f_color = v_color[0];
    normal = N;
    EmitVertex();

    gl_Position = v4;
    f_color = v_color[0];
    normal = N;
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
