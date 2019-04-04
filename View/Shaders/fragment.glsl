#version 150
#extension GL_ARB_separate_shader_objects : enable

layout (location = 1) in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
