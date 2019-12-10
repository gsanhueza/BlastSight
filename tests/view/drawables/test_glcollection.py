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

        assert len(collection) == 0

    def test_add(self):
        collection = GLCollection()
        collection.add(self.drawable)
        assert len(collection) == 1
        assert collection[0] == self.drawable

        drawable = collection[0]
        assert drawable == collection[0]
        assert isinstance(drawable, GLDrawable)
        assert isinstance(drawable.id, int)

    def test_set(self):
        collection = GLCollection()
        collection.add(self.drawable)
        drawable = collection[0]
        collection[0] = drawable

        assert isinstance(drawable, GLDrawable)
        assert isinstance(drawable.id, int)

    def test_delete(self):
        collection = GLCollection()
        collection.add(self.drawable)
        assert len(collection) == 1
        del collection[0]
        assert len(collection) == 0

    def test_items(self):
        collection = GLCollection()
        collection.add(self.drawable)
        drawable = collection[0]

        items = list(collection.items())
        assert items[0][0] == 0
        assert items[0][1] is drawable

    def test_clear(self):
        collection = GLCollection()
        collection.add(self.drawable)
        collection.add(self.drawable)
        collection.add(self.drawable)

        assert len(collection) == 1
        collection.clear()
        assert len(collection) == 0

    def test_drawable_collection(self):
        widget = IntegrableViewer()
        collection = GLDrawableCollection()
        drawable_1 = GLDrawable(self.element)
        drawable_2 = GLDrawable(self.element)

        collection.add(drawable_1)
        collection.add(drawable_2)

        assert collection.needs_update
        collection.draw(widget.proj, widget.camera, widget.world)
        assert not collection.needs_update
        collection.draw(widget.proj, widget.camera, widget.world)
        assert not collection.needs_update

        collection.recreate()
        assert collection.needs_update
        collection.draw(widget.proj, widget.camera, widget.world)
        assert not collection.needs_update
