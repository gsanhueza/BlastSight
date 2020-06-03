#!/usr/bin/env python

from blastsight.model.elements.element import Element
from blastsight.view.drawables.gldrawable import GLDrawable
from blastsight.view.collections.glcollection import GLCollection
from blastsight.view.integrableviewer import IntegrableViewer


class TestGLCollection:
    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0
    drawable = GLDrawable(element)

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
        assert isinstance(drawable, GLDrawable)
        assert isinstance(drawable.id, int)

    def test_get(self):
        collection = GLCollection()
        assert collection.size() == 0

        collection.add(self.drawable)

        assert collection.size() == 1
        assert collection.get_all_ids()[0] == collection.get_all_ids()[-1] == 0
        assert self.drawable in collection.get_all_drawables()

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

    def test_drawable_collection(self):
        # FIXME Why is this test here? Shouldn't it be in another file?
        viewer = IntegrableViewer()
        collection = viewer.drawable_collection

        collection.initialize()

        element_1 = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], alpha=1.0)
        element_2 = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0], alpha=0.5)

        drawable_1 = GLDrawable(element_1)
        drawable_2 = GLDrawable(element_2)

        collection.add(drawable_1)
        collection.add(drawable_2)

        assert collection._needs_update
        collection.draw()
        assert not collection._needs_update
        collection.draw()
        assert not collection._needs_update

        collection.recreate()
        assert collection._needs_update
        collection.draw()
        assert not collection._needs_update
