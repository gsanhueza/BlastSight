#version 120

varying highp vec3 f_color;

void main() {
    gl_FragColor = vec4(f_color, 0.0);
}
