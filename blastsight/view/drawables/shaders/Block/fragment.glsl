#version 330

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
    vec3 light_vector_front = vec3(0.0, 0.0, 1.0);
    vec3 light_vector_up = vec3(0.0, 1.0, 0.0);
    vec3 light_color = f_color;

    float front_bias = 0.9;
    vec3 ambient_light = vec3(0.1);
    vec3 color_front = front_bias * lambert(v_normal, light_vector_front, light_color);
    vec3 color_up = (1.0 - front_bias) * lambert(v_normal, light_vector_up, light_color);

    out_color = vec4(ambient_light + color_front + color_up, f_alpha);
}
