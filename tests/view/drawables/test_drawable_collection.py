#!/usr/bin/env python

import pytest
from minevis.model.elements.element import Element
from minevis.view.drawables.gldrawablecollection import GLDrawableCollection
from minevis.view.drawables.gldrawable import GLDrawable
from minevis.view.gui.integrableviewer import IntegrableViewer


class TestGLDrawableCollection:
    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    element.id = 0
    drawable = GLDrawable(widget=IntegrableViewer(), element=element)

    def test_base(self):
        collection = GLDrawableCollection()

        assert len(collection) == 0

    def test_add(self):
        collection = GLDrawableCollection()
        collection.add(self.drawable)
        assert len(collection) == 1
        assert collection[0] == self.drawable

        drawable = collection[0]
        assert drawable == collection[0]
        assert isinstance(drawable, GLDrawable)
        assert isinstance(drawable.id, int)

    def test_set(self):
        collection = GLDrawableCollection()
        collection.add(self.drawable)
        drawable = collection[0]
        collection[0] = drawable

        assert isinstance(drawable, GLDrawable)
        assert isinstance(drawable.id, int)

    def test_delete(self):
        collection = GLDrawableCollection()
        collection.add(self.drawable)
        assert len(collection) == 1
        del collection[0]
        assert len(collection) == 0

    def test_items(self):
        collection = GLDrawableCollection()
        collection.add(self.drawable)
        drawable = collection[0]

        items = list(collection.items())
        assert items[0][0] == 0
        assert items[0][1] is drawable

    def test_clear(self):
        collection = GLDrawableCollection()
        collection.add(self.drawable)
        collection.add(self.drawable)
        collection.add(self.drawable)

        assert len(collection) == 1
        collection.clear()
        assert len(collection) == 0

    def test_draw(self):
        widget = IntegrableViewer()
        collection = GLDrawableCollection(widget)
        drawable_1 = GLDrawable(widget, element=self.element)
        drawable_2 = GLDrawable(widget, element=self.element)

        with pytest.raises(Exception):
            drawable_1.initialize()
            drawable_2.initialize()

        collection.add(drawable_1)
        collection.add(drawable_2)
        collection.draw(widget.proj, widget.camera, widget.world)
