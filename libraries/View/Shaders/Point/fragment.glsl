#version 140

uniform vec2 min_max;
in float v_color;

out vec4 out_color;

float normalize_clamp(float x, float vmin, float vmax)
{
    float clamped = clamp(x, vmin, vmax);
    float epsilon = 0.0001;
    if (abs(vmax - vmin) < epsilon)
    {
        return 0.0;
    }
    return (clamped - vmin) / (vmax - vmin);
}

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main()
{
    vec3 light_color = hsv2rgb(vec3(2.0 / 3.0 * (1.0 - normalize_clamp(v_color, min_max.x, min_max.y)), 1.0, 1.0));
    out_color = vec4(light_color, 1.0);
}
