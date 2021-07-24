#version 140
#extension GL_ARB_explicit_attrib_location : require

in vec3 f_pos_mv;
in vec4 f_color;
in vec3 f_normal;

out vec4 out_color;

vec3 lambert(vec3 N, vec3 L, vec3 color)
{
    return color * max(dot(normalize(N), normalize(L)), 0.0);
}

void main()
{
    vec3 light_vector = vec3(0.0, 0.0, 1.0);
    vec3 col = lambert(f_normal, light_vector, f_color.rgb);
    vec3 ambient_light = vec3(0.1);

    out_color = vec4(ambient_light + col, f_color.a);
}
