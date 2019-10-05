#version 330

in vec4 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color.xyz, 1.0);
}
