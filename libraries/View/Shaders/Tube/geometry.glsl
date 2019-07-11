#version 150
#extension GL_EXT_geometry_shader4 : enable

#define M_PI 3.1415926535897932384626433832795

//uniform float radius;
//uniform int resolution;

const float radius = 0.15;  // FIXME This should come as uniform
const int resolution = 15;  // FIXME This should come as uniform too

layout (lines) in;
layout (triangle_strip, max_vertices = 90) out;

// max_vertices = 6 * resolution, where resolution is a uniform
// If resolution == 3, we should create 6 triangles to form the cylinder (prism)

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

in vec3 v_color[2];
out vec3 f_color;

in vec4 v_position[2];
out vec3 f_pos_mv;

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

void main()
{
    vec4 normal = normalize(v_position[1] - v_position[0]);
    vec4 tangent = vec4(normal.y, -normal.x, normal.zw);

    mat4 MVP = proj_matrix * model_view_matrix;

    for (int res = 0; res < resolution; res++)
    {
        mat4 rot_matrix = rotationMatrix(normal.xyz, 2 * M_PI * res / resolution);
        vec4 translated = radius * (rot_matrix * tangent);

        mat4 rot_matrix2 = rotationMatrix(normal.xyz, 2 * M_PI * (res + 1) / resolution);
        vec4 translated2 = radius * (rot_matrix2 * tangent);

        vec4 pos = v_position[0] + translated2;

        // Triangle A
        gl_Position = MVP * pos;
        f_pos_mv = (model_view_matrix * pos).xyz;
        f_color = v_color[0];
        EmitVertex();

        pos = v_position[1] + translated2;
        gl_Position = MVP * pos;
        f_pos_mv = (model_view_matrix * pos).xyz;
        f_color = v_color[0];
        EmitVertex();

        pos = v_position[1] + translated;
        gl_Position = MVP * pos;
        f_pos_mv = (model_view_matrix * pos).xyz;
        f_color = v_color[0];
        EmitVertex();

        EndPrimitive();

        // Triangle B
        pos = v_position[1] + translated;
        gl_Position = MVP * pos;
        f_pos_mv = (model_view_matrix * pos).xyz;
        f_color = v_color[0];
        EmitVertex();

        pos = v_position[0] + translated;
        gl_Position = MVP * pos;
        f_pos_mv = (model_view_matrix * pos).xyz;
        f_color = v_color[0];
        EmitVertex();

        pos = v_position[0] + translated2;
        gl_Position = MVP * pos;
        f_pos_mv = (model_view_matrix * pos).xyz;
        f_color = v_color[0];
        EmitVertex();

        EndPrimitive();
    }
}
