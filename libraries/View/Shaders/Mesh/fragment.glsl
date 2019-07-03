#version 150

in vec3 pos_mv;
in vec4 v_color;
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
    vec3 X = dFdx(pos_mv);
    vec3 Y = dFdy(pos_mv);
    vec3 v_normal = normalize(cross(X, Y));

    vec3 light_position = vec3(0.0, 0.0, 1000.0);
    vec3 col = lambert(v_normal, light_position, v_color.rgb);
    vec3 ambient_light = vec3(0.1);

    out_color = vec4(ambient_light + col, v_color.a);
}
