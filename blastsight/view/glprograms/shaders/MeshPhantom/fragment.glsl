#version 140
#extension GL_ARB_explicit_attrib_location : require

in vec3 pos_mv;
in vec4 v_color;
out vec4 out_color;

vec3 lambert(vec3 N, vec3 L, vec3 color)
{
    return color * max(dot(normalize(N), normalize(L)), 0.0);
}

void main()
{
    vec3 X = dFdx(pos_mv);
    vec3 Y = dFdy(pos_mv);
    vec3 v_normal = normalize(cross(X, Y));

    vec3 light_vector = vec3(0.0, 0.0, 1.0);
    vec3 col = lambert(v_normal, light_vector, v_color.rgb);
    vec3 ambient_light = vec3(0.1);
    out_color = vec4(ambient_light + col, 0.1);  // Enforce transparency
}
