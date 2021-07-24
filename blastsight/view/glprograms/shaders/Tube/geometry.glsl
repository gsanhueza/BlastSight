#version 150
#extension GL_EXT_geometry_shader4 : enable

#define M_PI 3.1415926535897932384626433832795

layout (lines) in;
layout (triangle_strip, max_vertices = 90) out;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

in vec4 v_color[2];
in vec4 v_position[2];
in vec2 v_properties[2];

out vec3 f_normal;
out vec4 f_color;

// Utilities
mat4 mvp = proj_matrix * model_view_matrix;
mat4 normal_matrix = transpose(inverse(model_view_matrix));

// Taken from http://www.neilmendoza.com/glsl-rotation-about-an-arbitrary-axis/
mat4 rotationMatrix(vec3 axis, float angle)
{
    axis = normalize(axis);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;

    return mat4(oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,  0.0,
                oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,  0.0,
                oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c,           0.0,
                0.0,                                0.0,                                0.0,                                1.0);
}

void emit_vertex(vec4 pos, vec4 normal)
{
    gl_Position = mvp * pos;
    f_color = v_color[0];
    f_normal = (normal_matrix * normal).xyz;
    EmitVertex();
}

void generate_circle(vec4 center, vec4 normal, vec4 tangent, float radius, int resolution)
{
    for (int res = 0; res <= resolution; res += 2)
    {
        mat4 rot_matrix_A = rotationMatrix(normal.xyz, 2 * M_PI * res / resolution);
        vec4 translated_A = radius * (rot_matrix_A * tangent);

        mat4 rot_matrix_B = rotationMatrix(normal.xyz, 2 * M_PI * (res + 1) / resolution);
        vec4 translated_B = radius * (rot_matrix_B * tangent);

        emit_vertex(center + translated_A, normal);
        emit_vertex(center + translated_B, normal);
        emit_vertex(center, normal);
    }

    EndPrimitive();
}

void generate_tube(vec4 pos_A, vec4 pos_B, vec4 normal, vec4 tangent, float radius, int resolution)
{
    for (int res = 0; res < resolution; res++)
    {
        mat4 rot_matrix_A = rotationMatrix(normal.xyz, 2 * M_PI * res / resolution);
        vec4 translated_A = radius * (rot_matrix_A * tangent);

        mat4 rot_matrix_B = rotationMatrix(normal.xyz, 2 * M_PI * (res + 1) / resolution);
        vec4 translated_B = radius * (rot_matrix_B * tangent);

        // Tube slice (2 triangles)
        emit_vertex(pos_A + translated_A, normalize(translated_A));
        emit_vertex(pos_A + translated_B, normalize(translated_B));
        emit_vertex(pos_B + translated_A, normalize(translated_A));
        emit_vertex(pos_B + translated_B, normalize(translated_B));

        EndPrimitive();
    }
}

void main()
{
    vec4 pos_A = v_position[0];
    vec4 pos_B = v_position[1];

    vec4 normal = normalize(pos_B - pos_A);
    vec4 tangent = vec4(normal.y, -normal.x, normal.z, normal.w);

    if (dot(normal, tangent) > 0.0001) {
        tangent = vec4(normal.z, normal.y, -normal.x, normal.w);
    }

    if (dot(normal, tangent) > 0.0001) {
        tangent = vec4(normal.x, normal.z, -normal.y, normal.w);
    }

    // Properties extraction (radius, resolution)
    float radius = v_properties[0].x;
    int resolution = clamp(int(v_properties[0].y), 3, 12);

    // Generate circle A
    generate_circle(pos_A, -normal, tangent, radius, resolution);

    // Generate circle B
    generate_circle(pos_B, normal, tangent, radius, resolution);

    // Generate tube sides
    generate_tube(pos_A, pos_B, normal, tangent, radius, resolution);
}
