#version 330
#extension GL_ARB_explicit_uniform_location : require

in vec3 v_color;
in vec2 v_texcoords;

out vec4 color;

layout (location = 0) uniform sampler2D text;

void main()
{
    vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, v_texcoords).r);
    color = vec4(v_color, 1.0) * sampled;
}
