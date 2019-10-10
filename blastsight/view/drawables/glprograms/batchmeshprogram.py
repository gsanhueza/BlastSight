#!/usr/bin/env python

import numpy as np
from OpenGL.GL import *

from .shaderprogram import ShaderProgram
from ..gldrawable import GLDrawable


class BatchMeshProgram(ShaderProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.base_name = 'Mesh'
        self.vaos = []
        self.vbos = []
        self.num_indices = 0
        self.already_set = False

    @property
    def vao(self):
        return self.vaos[-1]

    def recreate(self) -> None:
        self.already_set = False

    def set_drawables(self, meshes):
        if self.already_set:
            return

        self.set_buffers(meshes)
        self.already_set = True

    def set_buffers(self, meshes):
        _POSITION = 0
        _COLOR = 1
        _WIREFRAME = 2

        # VBO
        if len(self.vbos) == 0:
            self.vaos = [glGenVertexArrays(1)]
            self.vbos = glGenBuffers(3)

        # Get the meshes that we'll really render
        meshes = [m for m in meshes if m.is_visible]
        if len(meshes) == 0:
            return

        # Data
        vertices = np.empty(len(meshes), np.ndarray)
        indices = np.empty(len(meshes), np.ndarray)
        colors = np.empty(len(meshes), np.ndarray)

        v_size = 0
        for index, mesh in enumerate(meshes):
            num_triangles = mesh.element.vertices.size // 3

            indices[index] = (mesh.element.indices + v_size)
            vertices[index] = mesh.element.vertices.astype(np.float32)
            colors[index] = np.tile(mesh.element.rgba, num_triangles).astype(np.float32)

            self.num_indices += (mesh.element.indices + v_size).size
            v_size += num_triangles

        vertices = np.concatenate(vertices)
        indices = np.concatenate(indices)
        colors = np.concatenate(colors)

        glBindVertexArray(self.vao)

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                      (_COLOR, 4, colors, GLfloat, GL_FLOAT),
                      ]

        # Recycle GLDrawable's fill buffers method
        GLDrawable.fill_buffers(properties, self.vbos)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbos[-1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.num_indices, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
