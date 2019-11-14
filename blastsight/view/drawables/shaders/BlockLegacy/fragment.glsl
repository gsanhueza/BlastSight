#version 140
#extension GL_ARB_explicit_attrib_location : require

in vec3 v_color;
in float v_alpha;
in vec3 pos_mv;

out vec4 out_color;

vec3 lambert(vec3 N, vec3 L, vec3 color)
{
    return color * max(dot(normalize(N), normalize(L)), 0.0);
}

void main()
{
    vec3 light_vector_front = vec3(0.0, 0.0, 1.0);
    vec3 light_vector_up = vec3(0.0, 1.0, 0.0);
    vec3 light_color = v_color;

    vec3 X = dFdx(pos_mv);
    vec3 Y = dFdy(pos_mv);
    vec3 v_normal = normalize(cross(X, Y));

    float front_bias = 0.9;
    vec3 ambient_light = vec3(0.1);
    vec3 color_front = front_bias * lambert(v_normal, light_vector_front, light_color);
    vec3 color_up = (1.0 - front_bias) * lambert(v_normal, light_vector_up, light_color);

    out_color = vec4(ambient_light + color_front + color_up, v_alpha);
}
