#version 150

in vec3 f_color;
in vec3 f_pos_mv;

out vec4 out_color;

vec3 lambert(vec3 N, vec3 L, vec3 color)
{
    return color * max(dot(normalize(N), normalize(L)), 0.0);
}

void main()
{
    vec3 X = dFdx(f_pos_mv);
    vec3 Y = dFdy(f_pos_mv);
    vec3 v_normal = cross(X, Y);

    vec3 light_position = vec3(0.0, 0.0, 1000.0);
    vec3 col = lambert(v_normal, light_position, f_color);
    vec3 ambient_light = vec3(0.1);

    out_color = vec4(ambient_light + col, 1.0);
}
