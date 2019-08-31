#!/usr/bin/env python

from OpenGL.GL import *


class GLDrawable:
    def __init__(self, widget, element, *args, **kwargs):
        assert widget
        assert element
        self._widget = widget
        self._element = element

        self.vaos = []
        self.vbos = []

        self.is_initialized = False
        self.is_visible = True

    @property
    def widget(self):
        return self._widget

    @property
    def element(self):
        return self._element

    @property
    def vao(self) -> int:
        # We already know that we have only one VAO.
        # But cleanup is easier if we have the VAO in a list.
        return self.vaos[-1]

    @property
    def id(self) -> int:
        return self.element.id

    @id.setter
    def id(self, _id: int) -> None:
        self.element.id = _id

    def initialize(self) -> None:
        self.setup_attributes()
        self.is_initialized = True

    def setup_attributes(self) -> None:
        raise NotImplementedError

    def create_vao_vbos(self, vbo_count):
        if len(self.vaos) == 0:
            self.vaos = [glGenVertexArrays(1)]
            self.vbos = glGenBuffers(vbo_count)

    def fill_buffers(self, buffer_properties: list) -> None:
        # buffer_properties = [(pointer, basesize, array, glsize, gltype)]

        for i, buf in enumerate(buffer_properties):
            pointer, basesize, array, glsize, gltype = buf
            glBindBuffer(GL_ARRAY_BUFFER, self.vbos[i])
            glBufferData(GL_ARRAY_BUFFER, sizeof(glsize) * array.size, array, GL_STATIC_DRAW)
            glVertexAttribPointer(pointer, basesize, gltype, False, 0, None)
            glEnableVertexAttribArray(pointer)

    def draw(self) -> None:
        if not self.is_initialized:
            self.initialize()

    def cleanup(self):
        if self.is_initialized:
            self.widget.makeCurrent()
            glDeleteBuffers(len(self.vbos), self.vbos)
            glDeleteVertexArrays(len(self.vaos), self.vaos)

    """
    Quick GLDrawable API
    """
    def show(self) -> None:
        self.is_visible = True

    def hide(self) -> None:
        self.is_visible = False

    def toggle_visibility(self) -> None:
        self.is_visible = not self.is_visible
