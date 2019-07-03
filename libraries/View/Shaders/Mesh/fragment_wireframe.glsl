#version 150

in vec4 g_color;
out vec4 out_color;

void main()
{
    out_color = vec4(g_color.xyz, 1.0);
}
