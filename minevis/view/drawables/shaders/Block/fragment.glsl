#version 150
#extension GL_ARB_separate_shader_objects : enable

in vec3 v_normal;
in vec3 f_color;
in float f_alpha;

out vec4 out_color;

vec3 lambert(vec3 N, vec3 L, vec3 color)
{
    return color * max(dot(normalize(N), normalize(L)), 0.0);
}

void main()
{
    vec3 light_position_front = vec3(0.0, 0.0, 100000.0);
    vec3 light_position_up = vec3(0.0, 100000.0, 0.0);
    vec3 light_color = f_color;

    float front_light_bias = 0.85;
    vec3 color_front = lambert(v_normal, light_position_front, light_color);
    vec3 color_up = lambert(v_normal, light_position_up, light_color);

    out_color = vec4(0.05 + (front_light_bias * color_front) + ((1 - front_light_bias) * color_up), f_alpha);
}
