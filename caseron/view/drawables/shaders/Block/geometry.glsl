#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 12) out;

in vec3 v_position[1];
in vec3 v_color[1];
in float v_alpha[1];

out vec3 v_normal;
out vec3 f_color;
out float f_alpha;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec3 block_size;

mat4 mvp = proj_matrix * model_view_matrix;

void AddQuad(vec4 center, vec4 shift, vec4 dy, vec4 dx, vec3 n)
{
    vec4 v1 = (center + shift) + (dx - dy);
    vec4 v2 = (center + shift) + (-dx - dy);
    vec4 v3 = (center + shift) + (dx + dy);
    vec4 v4 = (center + shift) + (-dx + dy);

    // In orthographic projection we have to fix our origin (center),
    // because every ray has the same direction
    if (proj_matrix[3][3] == 1.0)
    {
        center = vec4(0.0, 0.0, -1.0, 1.0);
    }

    // Emit a primitive only if the sign of the dot product is positive
    vec4 normal = (model_view_matrix * vec4(n, 0.0));

    if (dot(-center.xyz, normal.xyz) > 0.0)
    {
        v_normal = normal.xyz;
        f_color = v_color[0];
        f_alpha = v_alpha[0];

        gl_Position = proj_matrix * v1;
        EmitVertex();

        gl_Position = proj_matrix * v2;
        EmitVertex();

        gl_Position = proj_matrix * v3;
        EmitVertex();

        gl_Position = proj_matrix * v4;
        EmitVertex();

        EndPrimitive();
    }
}

void main()
{
    vec4 center = model_view_matrix * vec4(v_position[0], 1.0);
    vec4 dx = 0.5f * model_view_matrix[0] * block_size.x;
    vec4 dy = 0.5f * model_view_matrix[1] * block_size.y;
    vec4 dz = 0.5f * model_view_matrix[2] * block_size.z;

    AddQuad(center, +dx, dy, dz, vec3(1.0, 0.0, 0.0));  // Right
    AddQuad(center, -dx, dz, dy, vec3(-1.0, 0.0, 0.0)); // Left
    AddQuad(center, +dy, dz, dx, vec3(0.0, 1.0, 0.0));  // Top
    AddQuad(center, -dy, dx, dz, vec3(0.0, -1.0, 0.0)); // Bottom
    AddQuad(center, +dz, dx, dy, vec3(0.0, 0.0, 1.0));  // Front
    AddQuad(center, -dz, dy, dx, vec3(0.0, 0.0, -1.0)); // Back
}
