#version 140
#extension GL_ARB_explicit_attrib_location : require

uniform int marker;
in vec3 v_color;
in float v_alpha;

out vec4 out_color;

vec3 lambert(vec3 N, vec3 L, vec3 color)
{
    return color * max(dot(normalize(N), normalize(L)), 0.0);
}

void main()
{
    /* A point is defined as a square [0.0, 1.0].
     * We need to move it to [-1.0, 1.0] and only if the pixel is inside
     * a circle of center (0.0, 0.0) and radius 1.0 we will draw it.
     *
     * Taken and adapted from:
     * https://stackoverflow.com/questions/17274820/drawing-round-points-using-modern-opengl
     */
    vec3 ambient_light = vec3(0.1);
    vec2 pos_screen = 2.0 * gl_PointCoord - vec2(1.0);
    vec3 col = v_color;

    switch(marker)
    {
    case 0:  // Square
        break;
    case 1:  // Circle
        if (length(pos_screen) > 1.0)
            discard;
        break;
    case 2:  // Sphere (impostor)
        if (length(pos_screen) > 1.0)
            discard;

        float normal_bias = 0.8;  // bias 1.0 => black on borders
        vec3 light_vector = vec3(0.0, 0.0, 1.0);
        vec3 v_normal = vec3(pos_screen.x, pos_screen.y, 1.0 - normal_bias * length(pos_screen));

        col = lambert(v_normal, light_vector, v_color);
    }

    out_color = vec4(ambient_light + col, v_alpha);
}
