#version 150
#extension GL_ARB_separate_shader_objects : enable

uniform vec3 u_color;
uniform vec2 u_alpha;

out vec4 out_color;

void main()
{
    out_color = vec4(u_color, u_alpha.x);
}
