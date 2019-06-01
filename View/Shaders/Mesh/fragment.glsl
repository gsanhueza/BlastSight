#version 150
#extension GL_ARB_separate_shader_objects : enable

in vec3 pos_mv;
out vec4 out_color;

uniform vec3 u_color;
uniform vec2 u_alpha;

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
    vec3 X = dFdx(pos_mv);
    vec3 Y = dFdy(pos_mv);
    vec3 v_normal = normalize(cross(X, Y));

    vec3 light_position = vec3(0.0, 0.0, 1000.0);
    vec3 col = lambert(v_normal, light_position, u_color);
    vec3 ambient_light = vec3(0.1);

    out_color = vec4(ambient_light + col, u_alpha.x);
}
