#version 150 core

layout(triangles) in;
layout(line_strip, max_vertices = 4) out;

in vec3 v_color[];
out vec3 f_color;

void main()
{
    for(int i = 0; i < gl_in.length(); i++) {
		gl_Position = gl_in[i].gl_Position;
        f_color = v_color[i];

		EmitVertex();
	}

    // Emit initial for the complete strip
    gl_Position = gl_in[0].gl_Position;
    f_color = v_color[0];

    EmitVertex();

	EndPrimitive();
}
