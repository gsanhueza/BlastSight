#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout (points) in;
layout (triangle_strip, max_vertices = 12) out;

in vec3 v_color[1];
in float v_alpha[1];

out vec3 v_normal;
out vec3 f_color;
out float f_alpha;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec3 block_size;

mat4 mvp = proj_matrix * model_view_matrix;

void AddQuad(vec4 center, vec4 dy, vec4 dx, vec3 n)
{
    vec4 v1 = center + (dx - dy);
    vec4 v2 = center + (-dx - dy);
    vec4 v3 = center + (dx + dy);
    vec4 v4 = center + (-dx + dy);

    // Emit a primitive only if the sign of the dot product is positive
    vec3 N = -(mvp * vec4(n, 0.0)).xyz;

    if (N.z > 0.0)
    {
        v_normal = N;
        f_color = v_color[0];
        f_alpha = v_alpha[0];

        gl_Position = v1;
        EmitVertex();

        gl_Position = v2;
        EmitVertex();

        gl_Position = v3;
        EmitVertex();

        gl_Position = v4;
        EmitVertex();

        EndPrimitive();
    }
}

void main()
{
    vec4 center = gl_in[0].gl_Position;

    vec4 dx = mvp[0] / 2.0f * block_size.x;
    vec4 dy = mvp[1] / 2.0f * block_size.y;
    vec4 dz = mvp[2] / 2.0f * block_size.z;
    AddQuad(center + dx, dy, dz, vec3(1.0, 0.0, 0.0)); // Right
    AddQuad(center - dx, dz, dy, vec3(-1.0, 0.0, 0.0)); // Left
    AddQuad(center + dy, dz, dx, vec3(0.0, 1.0, 0.0)); // Top
    AddQuad(center - dy, dx, dz, vec3(0.0, -1.0, 0.0)); // Bottom
    AddQuad(center + dz, dx, dy, vec3(0.0, 0.0, 1.0)); // Front
    AddQuad(center - dz, dy, dx, vec3(0.0, 0.0, -1.0)); // Back
}
