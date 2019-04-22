#version 150
#extension GL_ARB_separate_shader_objects : enable

layout (location = 1) in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(0.1, 0.9, 0.0, 1.0);
}
