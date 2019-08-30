#!/usr/bin/env python

from OpenGL.GL import *


class GLDrawable:
    def __init__(self, widget, element, *args, **kwargs):
        assert widget
        assert element
        self._widget = widget
        self._element = element

        self.vao = None
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

    def draw(self) -> None:
        if not self.is_initialized:
            self.initialize()

    def cleanup(self):
        if self.is_initialized:
            self.widget.makeCurrent()
            glDeleteBuffers(len(self.vbos), self.vbos)
            if self.vao is not None:
                glDeleteVertexArrays(1, int(self.vao))

    """
    Quick GLDrawable API
    """
    def show(self) -> None:
        self.is_visible = True

    def hide(self) -> None:
        self.is_visible = False

    def toggle_visibility(self) -> None:
        self.is_visible = not self.is_visible
