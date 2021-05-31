#version 330

layout (points) in;
layout (points, max_vertices = 1) out;

in vec3 v_position[1];
in vec3 v_color[1];
in float v_alpha[1];

out vec3 v_normal;
out vec3 f_color;
out float f_alpha;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec3 block_size;
uniform vec2 viewport;

uniform vec3 plane_origin;
uniform vec3 plane_normal;
uniform vec3 rendering_offset;

float EPSILON = 1e-6;

void main()
{
    // TODO Generate all edges
    // TODO Intersect them all, to get the vertices
    // TODO Generate a collection of triangles using the intersected vertices
    // TODO Emit them to generate triangles in real-time
    f_color = v_color[0];
    f_alpha = v_alpha[0];

    float plane_d = -dot(plane_normal, plane_origin);
    float threshold = dot(abs(plane_normal), block_size / 2);

    // TODO Delete this when the surface is ready
    float point_size = block_size[0];

    // Check if the "block" can be sliced with the plane equation
    if (abs(dot(plane_normal, v_position[0]) + plane_d) <= threshold)
    {
        gl_Position = proj_matrix * model_view_matrix * vec4(v_position[0] + rendering_offset, 1.0);

        // Perspective / Orthographic
        if (proj_matrix[3][3] == 0.0)
            gl_PointSize = 1.21 * viewport.y * point_size / gl_Position.w;
        else
            gl_PointSize = 0.5 * viewport.y * point_size * proj_matrix[1][1];

        EmitVertex();
    }

    EndPrimitive();
}
