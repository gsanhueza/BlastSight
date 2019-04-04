#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout(triangles) in;
layout(line_strip, max_vertices = 4) out;

in vec3 v_color[3];
out layout(location=1) vec3 f_color;

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
