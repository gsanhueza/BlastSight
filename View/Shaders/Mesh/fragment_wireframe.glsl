#version 120

uniform vec3 u_color;
uniform vec2 u_alpha;

void main()
{
    gl_FragColor = vec4(u_color, u_alpha);
}
