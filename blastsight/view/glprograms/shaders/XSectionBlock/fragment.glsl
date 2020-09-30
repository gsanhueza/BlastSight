#version 140
#extension GL_ARB_explicit_attrib_location : require

in vec3 f_color;
in float f_alpha;
out vec4 out_color;


void main()
{
    out_color = vec4(f_color, 1.0);
}
