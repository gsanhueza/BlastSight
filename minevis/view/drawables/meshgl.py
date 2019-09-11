#!/usr/bin/env python

import numpy as np
from OpenGL.GL import *

from .gldrawable import GLDrawable


class MeshGL(GLDrawable):
    def __init__(self, widget, element, *args, **kwargs):
        super().__init__(widget, element)
        self.indices_size = 0

        self.is_highlighted = kwargs.get('highlight', False)
        self.is_wireframed = kwargs.get('wireframe', False)

    def toggle_highlighting(self) -> bool:
        self.is_highlighted = not self.is_highlighted
        return self.is_highlighted

    def toggle_wireframe(self) -> bool:
        self.is_wireframed = not self.is_wireframed

        # Against our original idea, here we do not want to fill the
        # buffers again until OpenGL is already rendering.
        if self.is_initialized:
            self.setup_attributes()
        return self.is_wireframed

    def disable_wireframe(self) -> None:
        self.is_wireframed = False
        if self.is_initialized:
            self.setup_attributes()

    def enable_wireframe(self):
        self.is_wireframed = True
        if self.is_initialized:
            self.setup_attributes()

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Generate VAO and VBOs (see GLDrawable)
        self.create_vao_vbos(3)

        # Data
        vertices = self.element.vertices.astype(np.float32)
        indices = self.element.indices.astype(np.uint32)
        colors = self.element.rgba.astype(np.float32)

        self.indices_size = indices.size

        self.widget.makeCurrent()
        glBindVertexArray(self.vao)

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        buffer_properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                             (_COLOR, 4, colors, GLfloat, GL_FLOAT),
                             ]

        # Fill buffers (see GLDrawable)
        self.fill_buffers(buffer_properties)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbos[-1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered
        # And guess what, we have just 1 instance, exactly what we wanted!
        glVertexAttribDivisor(_COLOR, 1)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
