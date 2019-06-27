#version 150

uniform vec4 u_color;
out vec4 out_color;

void main()
{
    out_color = vec4(u_color.xyz, 1.0);
}
