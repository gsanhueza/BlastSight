#version 150
#extension GL_ARB_separate_shader_objects : enable

layout (location = 1) in vec3 v_color;
layout (location = 2) in vec3 v_pos_mv;

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
    vec3 X = dFdx(v_pos_mv);
    vec3 Y = dFdy(v_pos_mv);
    vec3 v_normal = normalize(cross(X, Y));

    vec3 light_position = vec3(0.0, 0.0, 1000.0);
//    vec3 light_color = v_color;
    vec3 light_color = vec3(0.0, 1.0, 0.0);

    vec3 col = lambert(v_normal, light_position, light_color);

    out_color = vec4(col, 1.0);
}