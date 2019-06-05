#version 150

in vec2 v_uv;
out vec4 frag_color;

void main()
{
    vec4 top_color = vec4(0.0, 0.0, 0.2, 1.0);
    vec4 bot_color = vec4(1.0);

    frag_color = bot_color * (1 - v_uv.y) + top_color * v_uv.y;
}