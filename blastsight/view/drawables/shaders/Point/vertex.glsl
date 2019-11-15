#version 140
#extension GL_ARB_explicit_attrib_location : require

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;
in float a_alpha;
in float point_size;

out vec3 v_color;
out float v_alpha;

uniform vec2 viewport;
uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    gl_Position = proj_matrix * model_view_matrix * vec4(a_position, 1.0);
    v_color = a_color;
    v_alpha = a_alpha;
    // The 1.21 factor was found by trial and error, with the goal of
    // allowing a squared point's "point_size" of `x` to appear extremely
    // similar to a cube's "block_size" of the same `x`.
    if (proj_matrix[3][3] == 0.0)
    {
        gl_PointSize = 1.21 * viewport.y * point_size / gl_Position.w;
    }
    else
    {
        // This is needed if an orthographic projection was selected.
        // We wouldn't want to see mega-points in the screen.
        gl_PointSize = 0.5 * viewport.y * point_size * proj_matrix[1][1];
    }
}
