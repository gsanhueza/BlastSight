#version 150
#extension GL_ARB_separate_shader_objects : enable

layout (location = 0) in vec3 v_position;
layout (location = 1) in vec3 v_color;
layout (location = 2) in vec3 v_normal;

out vec4 out_color;

void main()
{
    float brightness = 100.0;
    vec3 eye_position = vec3(0.0, 0.0, 0.0);
    vec3 light_position = vec3(0.0, 0.0, -10.0);
    vec3 light_color = v_color;

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
//
//    out_color = vec4(v_color, 1.0);
}
