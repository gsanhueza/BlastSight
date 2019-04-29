#version 150
#extension GL_ARB_separate_shader_objects : enable

layout (location = 1) in vec3 v_color;

out vec4 out_color;

void main()
{
    vec3 wireframe_color = vec3(0.1, 0.9, 0.0);
    out_color = vec4(wireframe_color, 1.0);
}
