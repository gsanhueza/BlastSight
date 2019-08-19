#version 140

uniform int marker;
in vec3 v_color;
in float v_alpha;

out vec4 out_color;

void main()
{
    /* A point is defined as a square [0, 1].
     * We need to move it to [-0.5, 0.5] and only if the pixel is inside a circle
     * of center (0, 0) and radius 0.5 we will draw it.
     * Taken from https://stackoverflow.com/questions/17274820/drawing-round-points-using-modern-opengl
     */
    if ((length(gl_PointCoord - vec2(0.5)) > 0.5) && marker > 0)
        discard;

    out_color = vec4(v_color, v_alpha);
}
