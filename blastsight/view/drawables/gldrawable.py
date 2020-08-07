#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *


class GLDrawable:
    def __init__(self, element, *args, **kwargs):
        # assert element
        super().__setattr__('element', element)  # self.element = element

        self._vaos = []
        self._vbos = []
        self._observers = []

        self._initialized = kwargs.pop('initialized', False)
        self._visible = kwargs.pop('visible', True)
        self._boostable = kwargs.pop('turbo', False)

    # Note: The following "hacks" are shortened versions of Delegator Pattern.
    # They're convenient, but optional.
    #
    # Example:
    # d = GLDrawable(element, *args, **kwargs)
    # assert d.alpha is d.element.alpha  => True
    def __dir__(self) -> list:
        # Hack to expose GLDrawable's attributes AND self.element's attributes
        # as if they were GLDrawable's attributes.
        # https://stackoverflow.com/q/15507848
        return list(set(super().__dir__() + dir(self.element)))

    def __getattribute__(self, attr: str) -> any:
        # Hack to get our attributes.
        # If not found, search self.element's attributes.
        # https://stackoverflow.com/a/2405617
        if hasattr(type(self), attr) or attr in super().__getattribute__('__dict__'):
            return super().__getattribute__(attr)
        return super().__getattribute__('element').__getattribute__(attr)

    def __setattr__(self, key, value) -> None:
        # Hack to set our attributes.
        # We'll try to set our element's attribute first, then ourselves.
        # https://stackoverflow.com/a/7042247
        if key in dir(self.element):
            self.element.__setattr__(key, value)
        else:
            super().__setattr__(key, value)

    @property
    def vao(self) -> int:
        # We already know that we have only one VAO.
        # But cleanup is easier if we have the VAO in a list.
        return self._vaos[-1]

    def initialize(self) -> None:
        if not self.is_initialized:
            self.setup_attributes()
        self.is_initialized = True

    def setup_attributes(self) -> None:
        pass

    def generate_buffers(self, vbo_count: int) -> None:
        if len(self._vaos) == 0:
            self._vaos = [glGenVertexArrays(1)]
            self._vbos = glGenBuffers(vbo_count)

    @staticmethod
    def fill_buffer(pointer, basesize, array, glsize, gltype, vbo):
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(glsize) * array.size, array, GL_STATIC_DRAW)
        glVertexAttribPointer(pointer, basesize, gltype, False, 0, None)
        glEnableVertexAttribArray(pointer)

    def draw(self) -> None:
        pass

    def cleanup(self) -> None:
        if self.is_initialized:
            glDeleteBuffers(len(self._vbos), self._vbos)
            glDeleteVertexArrays(len(self._vaos), self._vaos)

    """
    Properties
    """
    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def is_visible(self) -> bool:
        return self._visible

    @property
    def is_boostable(self) -> bool:
        return self._boostable

    @is_initialized.setter
    def is_initialized(self, status: bool) -> None:
        self._initialized = status

    @is_visible.setter
    def is_visible(self, status: bool) -> None:
        self._visible = status
        self.notify()

    @is_boostable.setter
    def is_boostable(self, status: bool) -> None:
        self._boostable = status
        self.notify()

    """
    Quick GLDrawable API
    """
    def add_observer(self, observer) -> None:
        self._observers.append(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.recreate()

    def show(self) -> None:
        self.is_visible = True

    def hide(self) -> None:
        self.is_visible = False

    def toggle_visibility(self) -> None:
        self.is_visible = not self.is_visible
