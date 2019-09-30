#!/usr/bin/env python

from OpenGL.GL import *


class GLDrawable(object):
    def __init__(self, element, *args, **kwargs):
        assert element
        self.element = element

        self.vaos = []
        self.vbos = []

        self.is_initialized = False
        self.is_highlighted = False
        self.is_visible = True

    def __dir__(self):
        # Hack to expose GLDrawable's attributes AND self.element's attributes
        # as if they were GLDrawable's attributes.
        # https://stackoverflow.com/q/15507848
        return sorted(set(dir(type(self)) + list(self.__dict__.keys()) + dir(self.element)))

    def __getattribute__(self, attr):
        # Hack to search our attributes.
        # If not found, search self.element's attributes.
        # https://stackoverflow.com/a/2405617
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            return self.element.__getattribute__(attr)

    @property
    def vao(self) -> int:
        # We already know that we have only one VAO.
        # But cleanup is easier if we have the VAO in a list.
        return self.vaos[-1]

    def initialize(self) -> None:
        self.setup_attributes()
        self.is_initialized = True

    def setup_attributes(self) -> None:
        pass

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
