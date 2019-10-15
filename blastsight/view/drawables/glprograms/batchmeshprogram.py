#!/usr/bin/env python

import numpy as np
from OpenGL.GL import *

from .meshprogram import MeshProgram
from ..gldrawable import GLDrawable


class BatchMeshProgram(MeshProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.vaos = []
        self.vbos = []
        self.v_size = 0
        self.num_indices = 0
        self.all_opaque = True

    @property
    def vao(self):
        return self.vaos[-1]

    def recreate(self) -> None:
        self.v_size = 0
        self.num_indices = 0
        self.all_opaque = True

    def set_drawables(self, meshes):
        self.drawables = meshes
        self.set_buffers()

    def set_buffers(self):
        _POSITION = 0
        _COLOR = 1
        _WIREFRAME = 2

        # VBO
        if len(self.vbos) == 0:
            self.vaos = [glGenVertexArrays(1)]
            self.vbos = glGenBuffers(3)

        # Get the meshes that we'll really render
        meshes = [m for m in self.drawables if m.is_visible]

        # Data
        vertices = np.empty(len(meshes), np.ndarray)
        indices = np.empty(len(meshes), np.ndarray)
        colors = np.empty(len(meshes), np.ndarray)

        for index, mesh in enumerate(meshes):
            num_triangles = mesh.element.vertices.size // 3

            indices[index] = (mesh.element.indices + self.v_size)
            vertices[index] = mesh.element.vertices.astype(np.float32)
            colors[index] = np.tile(mesh.element.rgba, num_triangles).astype(np.float32)

            self.num_indices += (mesh.element.indices + self.v_size).size
            self.v_size += num_triangles

            if mesh.alpha < 0.99:
                self.all_opaque = False

        if len(meshes) > 0:
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

        # We can perform faster if we don't need to fix alpha rendering
        if self.all_opaque:
            glDrawElements(GL_TRIANGLES, self.num_indices, GL_UNSIGNED_INT, None)
        else:
            glDepthMask(GL_FALSE)
            glEnable(GL_CULL_FACE)

            for gl_cull in [GL_FRONT, GL_BACK]:
                glCullFace(gl_cull)
                glDrawElements(GL_TRIANGLES, self.num_indices, GL_UNSIGNED_INT, None)

            glDisable(GL_CULL_FACE)
            glDepthMask(GL_TRUE)
