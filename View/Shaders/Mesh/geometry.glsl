#version 150
#extension GL_ARB_separate_shader_objects : enable
#extension GL_EXT_geometry_shader4 : enable

layout (triangles) in;
layout (line_strip, max_vertices = 4) out;

layout (location = 1) in vec3 pos_vm[3];
layout (location = 1) out vec3 v_pos_vm;

void main()
{
    for(int i = 0; i < gl_in.length(); i++) {
		gl_Position = gl_in[i].gl_Position;
        v_pos_vm = pos_vm[i];
		EmitVertex();
	}

    // Emit initial for the complete strip
    gl_Position = gl_in[0].gl_Position;
    v_pos_vm = pos_vm[0];

    EmitVertex();

	EndPrimitive();
}
