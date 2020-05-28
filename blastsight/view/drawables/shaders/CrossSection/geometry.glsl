#version 330

layout (triangles) in;
layout (line_strip, max_vertices = 2) out;

in vec3 v_position[3];
in vec4 v_color[3];

out vec4 f_color;

uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;
uniform vec3 plane_origin;
uniform vec3 plane_normal;

float EPSILON = 1e-6;

bool is_between(vec3 v_a, vec3 v_b, vec3 point)
{
    return distance(v_a, point) <= distance(v_a, v_b);
}

void emit_vertex(vec3 pos, vec4 color)
{
    gl_Position = proj_matrix * model_view_matrix * vec4(pos, 1.0);
    f_color = color;

    EmitVertex();
}

// Detect which edges intersect with the plane, and emit the intersection vertices
void emit_intersections(vec3 v_a, vec3 v_b, vec4 color)
{
    vec3 line_direction = normalize(v_b - v_a);

    float diff_dot_n = dot(plane_origin - v_a, plane_normal);
    float l_dot_n = dot(line_direction, plane_normal);

    if (abs(l_dot_n) < EPSILON)
    {
        if (abs(diff_dot_n) < EPSILON)  // Line completely contained in plane
        {
            emit_vertex(v_a, color);
            emit_vertex(v_b, color);
        }
        else; // Not a single point of intersection (the ';' is deliberately put there)
    }
    else  // Single point of intersection
    {
        float t = diff_dot_n / l_dot_n;
        vec3 intersection = v_a + t * line_direction;

        if (t >= 0.0 && is_between(v_a, v_b, intersection))
        {
            emit_vertex(intersection, color);
        }
    }
}

void main()
{
    for (int i = 0; i < gl_in.length(); i++)
    {
        emit_intersections(v_position[i], v_position[(i + 1) % gl_in.length()], v_color[i]);
    }

    EndPrimitive();
}
