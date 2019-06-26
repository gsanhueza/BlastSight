#!/usr/bin/env python

import pathlib


class GLDrawable:
    def __init__(self, widget, element):
        assert widget
        assert element
        self._widget = widget
        self._element = element
        self._shader_dir = f'{pathlib.Path(__file__).parent}/../Shaders'

        # Shader program
        self._shader_program = None

        # Vertex Array Object
        self.vao = None

        # Uniforms
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None

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

    @property
    def shader_program(self):
        return self._shader_program

    @shader_program.setter
    def shader_program(self, program) -> None:
        self._shader_program = program

    def initialize(self) -> None:
        self.initialize_program()
        self.initialize_shaders()
        self.setup_attributes()
        self.setup_uniforms()

        self.is_initialized = True

    def initialize_program(self) -> None:
        pass

    def initialize_shaders(self) -> None:
        pass

    def setup_attributes(self) -> None:
        pass

    def setup_uniforms(self) -> None:
        pass

    def draw(self, proj_matrix=None, view_matrix=None, model_matrix=None) -> None:
        if not self.is_initialized:
            self.initialize()

    """
    API for QTreeWidgetItem
    """
    def show(self) -> None:
        self.is_visible = True

    def hide(self) -> None:
        self.is_visible = False
