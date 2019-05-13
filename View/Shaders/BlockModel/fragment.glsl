#version 150
#extension GL_ARB_separate_shader_objects : enable

layout (location = 0) in vec3 v_position;
layout (location = 1) in vec3 v_color;
layout (location = 2) in vec3 v_normal;

out vec4 out_color;

float lambertian(vec3 N, vec3 L)
{
    vec3 normalized_N = normalize(N);
    vec3 normalized_L = normalize(L);
    return max(dot(normalized_N, normalized_L), 0.0);
}

vec3 lambert(vec3 N, vec3 L, vec3 color)
{
    return color * lambertian(N, L);
}

void main()
{
    vec3 light_position = vec3(0.0, 0.0, -10.0);
    vec3 light_color = v_color;

    vec3 col = lambert(v_normal, light_position, light_color);

    out_color = vec4(0.05 + col, 1.0);
    out_color = vec4(v_color, 1.0);
}
