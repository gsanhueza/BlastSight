#version 140
#extension GL_ARB_explicit_attrib_location : require

out vec2 v_uv;

// Taken from http://www.cs.princeton.edu/~mhalber/blog/ogl_gradient/
void main()
{
    int idx = gl_VertexID;
    gl_Position = vec4( idx & 1, idx >> 1, 0.0, 0.5 ) * 4.0 - 1.0;
    v_uv = vec2( gl_Position.xy * 0.5 + 0.5 );
}
