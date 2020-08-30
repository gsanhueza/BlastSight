#version 140
#extension GL_ARB_explicit_attrib_location : require

in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
