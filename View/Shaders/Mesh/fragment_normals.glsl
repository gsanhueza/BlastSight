#version 150
#extension GL_ARB_separate_shader_objects : enable

layout (location = 0) in vec3 v_position;
layout (location = 1) in vec3 v_color;
//layout (location = 2) in vec3 v_normal;
layout (location = 3) in vec3 v_pos_mv;

out vec4 out_color;

void main()
{
    vec3 X = dFdx(v_pos_mv);
    vec3 Y = dFdy(v_pos_mv);
    vec3 v_normal = normalize(cross(X, Y));

    float brightness = 1.0;
    vec3 eye_position = vec3(0.0, 0.0, -100.0);
    vec3 light_position = vec3(0.0, 0.0, -100.0);
    vec3 light_color = vec3(0.1, 0.9, 0.0);

    vec3 light_vector = normalize(light_position - v_position);
    vec3 reflected_light = reflect(light_vector, v_normal);
    vec3 eye_vector = normalize(eye_position - v_position);

    // Diffuse
    float Idiff = max(dot(v_normal, light_vector), 0.0);

    // Specular
    float Ispec = pow(max(dot(eye_vector, reflected_light), 0.0), brightness);

    // Ambient
    float Iamb = 0.2;

    out_color = vec4(light_color * (Idiff + Ispec + Iamb), 1.0);

}
