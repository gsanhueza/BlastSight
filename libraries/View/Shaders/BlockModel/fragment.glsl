#version 150
#extension GL_ARB_separate_shader_objects : enable

in float f_color;
in vec3 v_normal;

out vec4 out_color;

uniform vec2 min_max;

float normalize_values(float min_val, float max_val, float x)
{
    if (max_val == min_val)
    {
        return 0.0;
    }
    return (x - min_val) / (max_val - min_val);
}

vec3 lambert(vec3 N, vec3 L, vec3 color)
{
    return color * max(dot(normalize(N), normalize(L)), 0.0);
}

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main()
{
    vec3 light_position_front = vec3(0.0, 0.0, 100000.0);
    vec3 light_position_up = vec3(0.0, 100000.0, 0.0);
    vec3 light_color = hsv2rgb(vec3(2.0 / 3.0 * (1.0 - normalize_values(min_max.x, min_max.y, f_color)), 1.0, 1.0));

    float front_light_bias = 0.85;
    vec3 color_front = lambert(v_normal, light_position_front, light_color);
    vec3 color_up = lambert(v_normal, light_position_up, light_color);

    out_color = vec4(0.05 + (front_light_bias * color_front) + ((1 - front_light_bias) * color_up), 1.0);
}
