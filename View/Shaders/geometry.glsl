#version 150 core

layout(triangles) in;
layout(line_strip, max_vertices = 3) out;

in vec3 v_color[];
out vec3 f_color;

void main()
{
    for(int i = 0; i < gl_in.length(); i++) {
		gl_Position = gl_in[i].gl_Position;
        f_color = v_color[i];

		EmitVertex();
	}

	EndPrimitive();
}
