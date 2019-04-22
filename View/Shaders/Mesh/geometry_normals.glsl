#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

layout (location = 1) in vec3 v_color[3];
layout (location = 1) out vec3 f_color;

layout (location = 2) out vec3 normal;

void main()
{
    vec3 a = (gl_in[1].gl_Position - gl_in[0].gl_Position).xyz;
    vec3 b = (gl_in[2].gl_Position - gl_in[0].gl_Position).xyz;
    vec3 N = normalize(cross(b, a));

    for (int i = 0; i < gl_in.length(); i++)
    {
        gl_Position = gl_in[i].gl_Position;
        f_color = v_color[i];
        normal = N;
        EmitVertex();
    }

    EndPrimitive();
}
