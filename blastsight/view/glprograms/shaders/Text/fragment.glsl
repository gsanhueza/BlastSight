#version 330
#extension GL_ARB_explicit_uniform_location : require

in vec2 TexCoords;
out vec4 color;

layout (location = 0) uniform sampler2D text;
//uniform vec3 textColor;
vec3 textColor = vec3(1.0, 1.0, 1.0);

void main()
{
    vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
    color = vec4(textColor, 1.0) * sampled;
}
