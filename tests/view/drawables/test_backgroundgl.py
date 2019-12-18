#!/usr/bin/env python

from blastsight.view.integrableviewer import IntegrableViewer
from blastsight.view.drawables.backgroundgl import BackgroundGL
from blastsight.view.glprograms.backgroundprogram import BackgroundProgram

from blastsight.model.elements.nullelement import NullElement


class TestBackgroundGL:
    def test_empty_bg(self):
        drawable = BackgroundGL()
        assert type(drawable.element) is NullElement

    def test_dir(self):
        assert len(dir(BackgroundGL(NullElement()))) > 0

    def test_draw(self):
        widget = IntegrableViewer()
        program = BackgroundProgram(widget)
        program.setup()
        program.bind()

        drawable = BackgroundGL(NullElement())

        drawable.hide()
        assert not drawable.is_visible
        drawable.draw()

        drawable.show()
        assert drawable.is_visible
        drawable.draw()

        drawable.hide()
        assert not drawable.is_visible

    def test_colors(self):
        widget = IntegrableViewer()
        program = BackgroundProgram(widget)
        program.setup()
        program.bind()

        drawable = BackgroundGL(NullElement())
        top = [0.1, 0.2, 0.3]
        bot = [0.4, 0.5, 0.6]

        for expect, result in zip(top, drawable.top_color):
            assert expect == result

        for expect, result in zip(bot, drawable.bot_color):
            assert expect == result

        top = [0.2, 0.4, 0.6]
        bot = [0.6, 0.4, 0.2]

        drawable.top_color = top
        drawable.bot_color = bot

        for expect, result in zip(top, drawable.top_color):
            assert expect == result

        for expect, result in zip(bot, drawable.bot_color):
            assert expect == result

    def test_program(self):
        widget = IntegrableViewer()
        program = BackgroundProgram(widget)
        program.setup()
        program.bind()

        assert len(program.drawables) == 0
        assert len(program.transparents) == 0

        drawable = BackgroundGL(NullElement())
        program.set_drawables([drawable])
        program.draw()

        assert len(program.drawables) > 0
        assert len(program.transparents) == 0
