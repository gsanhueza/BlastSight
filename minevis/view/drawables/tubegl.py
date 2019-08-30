#!/usr/bin/env python

import numpy as np

from .gldrawable import GLDrawable
from OpenGL.GL import *


class TubeGL(GLDrawable):
    def __init__(self, widget, element, *args, **kwargs):
        super().__init__(widget, element)

        self.indices_size = 0

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        if self.vao is None:
            self.vao = glGenVertexArrays(1)
            self.vbos = glGenBuffers(3)

        # Data
        vertices, indices = self.element.as_mesh()

        vertices = np.array(vertices).astype(np.float32)
        indices = np.array(indices).astype(np.uint32)
        colors = self.element.rgba.astype(np.float32)

        self.indices_size = indices.size

        self.widget.makeCurrent()
        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[0])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * vertices.size, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbos[1])
        glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * colors.size, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 4, GL_FLOAT, False, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbos[2])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered
        # And guess what, we have just 1 instance, exactly what we wanted!
        glVertexAttribDivisor(_COLOR, 1)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
