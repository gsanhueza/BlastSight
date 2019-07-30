#!/usr/bin/env python

from OpenGL.GL import *


class GLDrawable:
    def __init__(self, widget, element):
        assert widget
        assert element
        self._widget = widget
        self._element = element

        self.vao = None
        self.vbos = []

        self.is_initialized = False
        self.is_visible = True

    @property
    def id(self) -> int:
        return self._element.id

    @id.setter
    def id(self, _id: int) -> None:
        self._element.id = _id

    @property
    def widget(self):
        return self._widget

    @property
    def element(self):
        return self._element

    def initialize(self) -> None:
        self.setup_attributes()
        self.is_initialized = True

    def setup_attributes(self) -> None:
        pass

    def draw(self) -> None:
        if not self.is_initialized:
            self.initialize()

    def cleanup(self):
        pass
    #     self.is_visible = False
    #     self.widget.makeCurrent()
    #     if self.vao:
    #         glBindVertexArray(self.vao)
    #     glDeleteBuffers(len(self.vbos), self.vbos)
    #     glBindVertexArray(0)
    #     del self.vbos
    #     del self.vao

    # This try/except catches an ImportError exception on glDeleteBuffers,
    # when the application is closed (either normally or suddenly).
    # Consider this as documentation that justifies the need to have
    # a try/except block in a destroyer (the original exception gets
    # ignored anyway, we're just silencing it here).
    # Unless there's a more elegant solution, this will have to suffice.
    #
    # Exception ignored in: <function GLDrawable.__del__ at 0x7f8c22aefae8>
    # Traceback (most recent call last):
    # File "/data/gabriel/Proyectos/MineVis/libraries/View/Drawables/gldrawable.py", line 48, in __del__
    # File "/usr/lib/python3.7/site-packages/OpenGL/wrapper.py", line 96, in __nonzero__
    # File "/usr/lib/python3.7/site-packages/OpenGL/platform/baseplatform.py", line 376, in __nonzero__
    # File "/usr/lib/python3.7/site-packages/OpenGL/platform/baseplatform.py", line 381, in load
    # ImportError: sys.meta_path is None, Python is likely shutting down
    def __del__(self):
        self.widget.makeCurrent()
        if self.vao is not None:
            glBindVertexArray(self.vao)
        glDeleteBuffers(len(self.vbos), self.vbos)
        glBindVertexArray(0)

    """
    API for QTreeWidgetItem
    """
    def show(self) -> None:
        self.is_visible = True

    def hide(self) -> None:
        self.is_visible = False

    def toggle_visibility(self) -> None:
        self.is_visible = not self.is_visible
