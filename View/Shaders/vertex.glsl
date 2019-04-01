attribute vec3 a_position;
attribute vec3 a_color;
varying vec3 v_color;

uniform int test_value;
uniform mat4 proj_matrix;
uniform mat4 model_view_matrix;

void main()
{
    proj_matrix = mat4( 1.0, 0.0, 0.0, 0.0,  // first column
                        0.0, 1.0, 0.0, 0.0,  // second column
                        0.0, 0.0, 1.0, 0.0,  // third column
                        0.0, 0.0, 0.0, 1.0); // fourth column

    model_view_matrix = mat4(   1.0, sin(test_value/100.0), 0.0, 0.0,  // first column
                                0.0, 1.0, 0.0, 0.0,  // second column
                                0.0, 0.0, 1.0, 0.0,  // third column
                                0.0, 0.0, 0.0, 1.0); // fourth column

    gl_Position = proj_matrix * model_view_matrix * vec4(a_position, 1.0);
    v_color = a_color;
}
