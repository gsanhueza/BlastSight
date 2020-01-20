#!/usr/bin/env python

from blastsight.model.elements.element import Element
from blastsight.view.drawables.gldrawable import GLDrawable
from blastsight.view.collections.glcollection import GLCollection
from blastsight.view.collections.gldrawablecollection import GLDrawableCollection
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

    def test_set(self):
        collection = GLCollection()
        collection.add(self.drawable)
        drawable = collection.get(0)
        collection.update(0, drawable)

        assert isinstance(drawable, GLDrawable)
        assert isinstance(drawable.id, int)

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
        widget = IntegrableViewer()
        collection = GLDrawableCollection()
        drawable_1 = GLDrawable(self.element)
        drawable_2 = GLDrawable(self.element)

        collection.add(drawable_1)
        collection.add(drawable_2)

        assert collection._needs_update
        collection.draw(widget.proj, widget.camera, widget.world)
        assert not collection._needs_update
        collection.draw(widget.proj, widget.camera, widget.world)
        assert not collection._needs_update

        collection.recreate()
        assert collection._needs_update
        collection.draw(widget.proj, widget.camera, widget.world)
        assert not collection._needs_update
