#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
from OpenGL.GL import *

from .meshprogram import MeshProgram
from ..drawables.gldrawable import GLDrawable


class TurboMeshProgram(MeshProgram):
    def __init__(self, widget):
        super().__init__(widget)
        self.info = {
            'opaque': {
                'vaos': [],
                'vbos': [],
                'v_size': 0,
                'num_indices': 0,
            },
            'transparent': {
                'vaos': [],
                'vbos': [],
                'v_size': 0,
                'num_indices': 0,
            },
        }

    def recreate(self) -> None:
        self.info['opaque']['v_size'] = 0
        self.info['opaque']['num_indices'] = 0
        self.info['transparent']['v_size'] = 0
        self.info['transparent']['num_indices'] = 0

    def set_drawables(self, drawables):
        super().set_drawables(drawables)
        self.set_buffers(self.drawables, 'opaque')
        self.set_buffers(self.transparents, 'transparent')

    def set_buffers(self, meshes, visibility):
        _POSITION = 0
        _COLOR = 1
        _WIREFRAME = 2

        # VBO
        if len(self.info[visibility]['vbos']) == 0:
            self.info[visibility]['vaos'] = [glGenVertexArrays(1)]
            self.info[visibility]['vbos'] = glGenBuffers(3)

        # Data
        vertices = np.empty(len(meshes), np.ndarray)
        indices = np.empty(len(meshes), np.ndarray)
        colors = np.empty(len(meshes), np.ndarray)

        for index, mesh in enumerate(meshes):
            num_triangles = mesh.element.vertices.size // 3

            indices[index] = (mesh.element.indices + self.info[visibility]['v_size'])
            vertices[index] = mesh.element.vertices.astype(np.float32)
            colors[index] = np.tile(mesh.element.rgba, num_triangles).astype(np.float32)

            self.info[visibility]['num_indices'] += (mesh.element.indices + self.info[visibility]['v_size']).size
            self.info[visibility]['v_size'] += num_triangles

        if len(meshes) > 0:
            vertices = np.concatenate(vertices)
            indices = np.concatenate(indices)
            colors = np.concatenate(colors)

        glBindVertexArray(self.info[visibility]['vaos'][-1])

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                      (_COLOR, 4, colors, GLfloat, GL_FLOAT),
                      ]

        # Recycle GLDrawable's fill buffers method
        GLDrawable.fill_buffers(properties, self.info[visibility]['vbos'])

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.info[visibility]['vbos'][-1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.info['opaque']['vaos'][-1])
        glDrawElements(GL_TRIANGLES, self.info['opaque']['num_indices'], GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def redraw(self):
        glBindVertexArray(self.info['transparent']['vaos'][-1])
        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)

        for gl_cull in [GL_FRONT, GL_BACK]:
            glCullFace(gl_cull)
            glDrawElements(GL_TRIANGLES, self.info['transparent']['num_indices'], GL_UNSIGNED_INT, None)

        glDisable(GL_CULL_FACE)
        glDepthMask(GL_TRUE)
        glBindVertexArray(0)
