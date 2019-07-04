#version 150
#extension GL_EXT_geometry_shader4 : enable

layout (triangles) in;
layout (line_strip, max_vertices = 4) out;

in vec4 v_color[3];
out vec4 g_color;

void main()
{
    // Less than **or equal** because we want to re-emit the initial vertex
    int length = gl_in.length();
    for(int i = 0; i <= length; i++) {
		gl_Position = gl_in[i % length].gl_Position;  // We'll emit 0, 1, 2, 0
		g_color = v_color[i % 3];
		EmitVertex();
	}

	EndPrimitive();
}
