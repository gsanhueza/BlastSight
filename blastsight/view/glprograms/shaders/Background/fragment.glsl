#version 140
#extension GL_ARB_explicit_attrib_location : require

uniform vec4 top_color;
uniform vec4 bottom_color;

in vec2 v_uv;
out vec4 out_color;

// Taken from http://www.cs.princeton.edu/~mhalber/blog/ogl_gradient/
void main()
{
    out_color = vec4(bottom_color * (1 - v_uv.y) + top_color * v_uv.y);
}
