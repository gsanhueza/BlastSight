#version 140

in vec3 v_color;
in float v_alpha;
in vec3 pos_mv;

out vec4 out_color;

uniform vec2 min_max;

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
    vec3 light_position_front = vec3(0.0, 0.0, 100000.0);
    vec3 light_position_up = vec3(0.0, 100000.0, 0.0);
    vec3 light_color = v_color;

    vec3 X = dFdx(pos_mv);
    vec3 Y = dFdy(pos_mv);
    vec3 v_normal = normalize(cross(X, Y));

    float front_light_bias = 0.85;
    vec3 color_front = lambert(v_normal, light_position_front, light_color);
    vec3 color_up = lambert(v_normal, light_position_up, light_color);

    out_color = vec4(0.05 + (front_light_bias * color_front) + ((1 - front_light_bias) * color_up), v_alpha);
}
