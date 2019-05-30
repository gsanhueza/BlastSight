#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout (lines) in;
layout (triangle_strip, max_vertices = 6) out;

layout (location = 1) in vec3 v_color[2];
layout (location = 1) out vec3 f_color;

void main()
{
    // Triangle A
    gl_Position = gl_in[0].gl_Position;
    f_color = v_color[0];
    EmitVertex();

    gl_Position = gl_in[1].gl_Position;
    f_color = v_color[0];
    EmitVertex();

    gl_Position = gl_in[1].gl_Position + vec4(0.0, 1.0, 0.0, 1.0);
    f_color = v_color[0];
    EmitVertex();

    EndPrimitive();

    // Triangle B
    gl_Position = gl_in[1].gl_Position + vec4(0.0, 1.0, 0.0, 1.0);
    f_color = v_color[0];
    EmitVertex();

    gl_Position = gl_in[0].gl_Position + vec4(0.0, 1.0, 0.0, 1.0);
    f_color = v_color[0];
    EmitVertex();

    gl_Position = gl_in[0].gl_Position;
    f_color = v_color[0];
    EmitVertex();

	EndPrimitive();
}
