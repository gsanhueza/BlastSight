#version 150
#extension GL_ARB_separate_shader_objects : enable

uniform vec3 u_color;
uniform vec2 u_alpha;

out vec4 out_color;

void main()
{
//    // WARNING For some reason we *need* to use u_color, or it segfaults
//    vec3 wireframe_color = u_color * 0.0000001 + vec3(0.1, 0.9, 0.0);
//    out_color = vec4(wireframe_color, 1.0);
    out_color = vec4(u_color, u_alpha.x);
}
