#version 120

attribute vec3 vertex;
attribute vec3 color;

varying vec3 f_color;

uniform mat4 projMatrix;
uniform mat4 modelViewMatrix;

void main(){
    f_color = color;
    gl_Position = projMatrix * modelViewMatrix * vec4(vertex, 1.0);
}
