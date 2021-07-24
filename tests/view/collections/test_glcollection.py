#!/usr/bin/env python

from blastsight.model.model import Model
from blastsight.view.drawablefactory import DrawableFactory

from blastsight.view.drawables.meshgl import MeshGL
from blastsight.view.drawables.blockgl import BlockGL
from blastsight.view.drawables.linegl import LineGL

from blastsight.view.collections.glcollection import GLCollection
from blastsight.view.glprograms.shaderprogram import ShaderProgram


class TestGLCollection:
    factory = DrawableFactory(Model())
    drawable = factory.lines(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], id=0)

    def test_base(self):
        collection = GLCollection()

        assert collection.size() == 0

    def test_add(self):
        collection = GLCollection()
        collection.add(self.drawable)
        assert collection.size() == 1
        assert collection.get(0) == self.drawable

        drawable = collection.get(0)
        assert drawable == collection.get(0)
        assert isinstance(drawable, LineGL)
        assert isinstance(drawable.id, int)

    def test_get(self):
        collection = GLCollection()
        assert collection.size() == 0

        collection.add(self.drawable)

        assert collection.size() == 1
        assert collection.all_ids()[0] == collection.all_ids()[-1] == 0
        assert self.drawable in collection.all_drawables()

        assert collection.get_last() is self.drawable

    def test_delete(self):
        collection = GLCollection()
        collection.add(self.drawable)
        assert collection.size() == 1
        collection.delete(0)
        assert collection.size() == 0

    def test_clear(self):
        collection = GLCollection()
        collection.add(self.drawable)
        collection.add(self.drawable)
        collection.add(self.drawable)

        assert collection.size() == 1
        collection.clear()
        assert collection.size() == 0

    def test_retriever(self):
        collection = GLCollection()

        mesh = self.factory.mesh(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], indices=[[0, 1, 2]], id=0)
        blocks = self.factory.blocks(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], values=[0, 1, 2], id=1)
        lines = self.factory.lines(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], id=2)

        collection.add(mesh)
        collection.add(blocks)
        collection.add(lines)

        # Remember that the element is a Line
        assert len(collection.select(MeshGL)) == 1
        assert len(collection.select(BlockGL,)) == 1
        assert len(collection.select(LineGL)) == 1

        assert len(collection.select(MeshGL, lambda x: x.is_standard)) == 1
        assert len(collection.select(MeshGL, lambda x: x.is_turbo_ready)) == 0
        assert len(collection.select(MeshGL, lambda x: x.is_highlighted)) == 0
        assert len(collection.select(MeshGL, lambda x: x.is_wireframed)) == 0
