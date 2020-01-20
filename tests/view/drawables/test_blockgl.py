#!/usr/bin/env python

import pytest

from blastsight.model.elements.blockelement import BlockElement
from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.drawables.blockgl import BlockGL
from blastsight.view.glprograms.blockprogram import BlockProgram
from blastsight.view.glprograms.blocklegacyprogram import BlockLegacyProgram


class TestBlockGL:
    element = BlockElement(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2])
    element.id = 0

    def test_empty_block(self):
        with pytest.raises(Exception):
            BlockGL()

    def test_block_base(self):
        drawable = BlockGL(self.element)

        assert drawable
        assert drawable.id == 0

        assert not drawable.is_initialized

    def test_block_initialize(self):
        drawable = BlockGL(self.element)
        assert not drawable.is_initialized

        drawable.initialize()

        assert drawable.is_initialized

    def test_draw(self):
        viewer = IntegrableViewer()
        program = BlockProgram(viewer)
        program.setup()
        program.bind()

        drawable = BlockGL(self.element)
        drawable.setup_attributes()

        program.set_drawables([drawable])
        program.draw()

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible

    def test_program(self):
        viewer = IntegrableViewer()
        program = BlockProgram(viewer)
        program.setup()
        program.bind()

        drawable = BlockGL(self.element)
        assert not drawable.is_legacy

        program.set_drawables([drawable])
        program.draw()

    def test_legacy_program(self):
        viewer = IntegrableViewer()
        program = BlockLegacyProgram(viewer)
        program.setup()
        program.bind()

        drawable = BlockGL(self.element, legacy=True)
        assert drawable.is_legacy
        program.set_drawables([drawable])
        program.draw()

        drawable.is_legacy = False
        assert not drawable.is_initialized
        program.set_drawables([drawable])
        program.draw()

        assert drawable.is_initialized
