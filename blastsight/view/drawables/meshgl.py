#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
from OpenGL.GL import *

from .gldrawable import GLDrawable


class MeshGL(GLDrawable):
    def __init__(self, element, *args, **kwargs):
        super().__init__(element, *args, **kwargs)
        self.indices_size = 0

        self._highlighted = kwargs.pop('highlight', False)
        self._wireframed = kwargs.pop('wireframe', False)
        self._cross_sectionable = kwargs.pop('cross_section', False)

    """
    Properties
    """
    @property
    def is_standard(self) -> bool:
        return not (self.is_wireframed or self.is_turbo_ready or self.is_cross_sectionable)

    @property
    def is_highlighted(self) -> bool:
        return self._highlighted

    @property
    def is_wireframed(self) -> bool:
        return self._wireframed

    @property
    def is_turbo_ready(self) -> bool:
        return self.is_boostable and not (self.is_highlighted or self.is_wireframed or self.is_cross_sectionable)

    @property
    def is_cross_sectionable(self) -> bool:
        return self._cross_sectionable

    @is_highlighted.setter
    def is_highlighted(self, status: bool) -> None:
        self._highlighted = status
        self.notify()

    @is_wireframed.setter
    def is_wireframed(self, status: bool) -> None:
        self._wireframed = status
        self.notify()

    @is_cross_sectionable.setter
    def is_cross_sectionable(self, status: bool) -> None:
        self._cross_sectionable = status
        self.notify()

    """
    Quick MeshGL API
    """
    def enable_highlighting(self) -> None:
        self.is_highlighted = True

    def disable_highlighting(self) -> None:
        self.is_highlighted = False

    def toggle_highlighting(self) -> bool:
        self.is_highlighted = not self.is_highlighted
        return self.is_highlighted

    def enable_wireframe(self) -> None:
        self.is_wireframed = True

    def disable_wireframe(self) -> None:
        self.is_wireframed = False

    def toggle_wireframe(self) -> bool:
        self.is_wireframed = not self.is_wireframed
        return self.is_wireframed

    """
    Internal methods
    """
    def setup_attributes(self) -> None:
        _POSITION = 0
        _COLOR = 1

        # Generate VAO and VBOs (see GLDrawable)
        self.generate_buffers(3)

        # Data
        vertices = self.element.vertices.astype(np.float32)
        indices = self.element.indices.astype(np.uint32)
        colors = self.element.rgba.astype(np.float32)

        self.indices_size = indices.size

        glBindVertexArray(self.vao)

        # Fill buffers (see GLDrawable)
        self.fill_buffer(_POSITION, 3, vertices, GLfloat, GL_FLOAT, self._vbos[_POSITION])
        self.fill_buffer(_COLOR, 4, colors, GLfloat, GL_FLOAT, self._vbos[_COLOR])

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._vbos[-1])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        # The attribute advances once per divisor instances of the set(s) of vertices being rendered
        # And guess what, we have just 1 instance, exactly what we wanted!
        glVertexAttribDivisor(_COLOR, 1)

        glBindVertexArray(0)

    def draw(self) -> None:
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.indices_size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
