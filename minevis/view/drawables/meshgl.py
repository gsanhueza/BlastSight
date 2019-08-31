#!/usr/bin/env python

import numpy as np
from OpenGL.GL import *

from .gldrawable import GLDrawable


class MeshGL(GLDrawable):
    def __init__(self, widget, element, *args, **kwargs):
        super().__init__(widget, element)

        # Size
        self.indices_size = 0

        # Wireframe
        self.wireframe_enabled = kwargs.get('wireframe', False)

    def toggle_wireframe(self) -> bool:
        self.wireframe_enabled = not self.wireframe_enabled

        # Against our original idea, here we do not want to fill the
        # buffers again until OpenGL is already rendering.
        if self.is_initialized:
            self.setup_attributes()
        return self.wireframe_enabled

    def disable_wireframe(self) -> None:
        self.wireframe_enabled = False
        if self.is_initialized:
            self.setup_attributes()

    def enable_wireframe(self):
        self.wireframe_enabled = True
        if self.is_initialized:
            self.setup_attributes()

    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1
        _WIREFRAME = 2

        # Generate VAO and VBOs (see GLDrawable)
        self.create_vao_vbos(4)

        # Data
        vertices = self.element.vertices.astype(np.float32)
        indices = self.element.indices.astype(np.uint32)
        colors = self.element.rgba.astype(np.float32)
        wireframe = np.array([1 if self.wireframe_enabled else 0], np.byte)

        self.indices_size = indices.size

        self.widget.makeCurrent()
        glBindVertexArray(self.vao)

        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]
        buffer_properties = [(_POSITION, 3, vertices, GLfloat, GL_FLOAT),
                             (_COLOR, 4, colors, GLfloat, GL_FLOAT),
                             (_WIREFRAME, 1, wireframe, GLbyte, GL_BYTE),
                             ]

        # Fill buffers (see GLDrawable)
        self.fill_buffers(buffer_properties)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbos[-1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered
        # And guess what, we have just 1 instance, exactly what we wanted!
        glVertexAttribDivisor(_COLOR, 1)
        glVertexAttribDivisor(_WIREFRAME, 1)

        glBindVertexArray(0)

    def draw(self):
        super().draw()
        if not self.is_visible:
            return

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
