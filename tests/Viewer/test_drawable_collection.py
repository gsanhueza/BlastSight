#!/usr/bin/env python

from Model.Elements.element import Element
from View.Drawables.drawablecollection import GLDrawableCollection
from View.Drawables.gldrawable import GLDrawable
from View.GUI.openglwidget import OpenGLWidget


class TestGLDrawableCollection:
    element = Element(x=[-1, 1, 0], y=[0, 0, 1], z=[0, 0, 0])
    drawable = GLDrawable(widget=OpenGLWidget(), element=element)
    drawable.id = 0

    def test_base(self):
        collection = GLDrawableCollection()

        assert len(collection) == 0

    def test_add(self):
        collection = GLDrawableCollection()
        collection.add(0, self.drawable)
        assert len(collection) == 1

        drawable = collection[0]
        assert isinstance(drawable, GLDrawable)
        assert isinstance(drawable.id, int)

    def test_set(self):
        collection = GLDrawableCollection()
        collection.add(0, self.drawable)
        drawable = collection[0]
        collection[0] = drawable

        assert isinstance(drawable, GLDrawable)
        assert isinstance(drawable.id, int)

    def test_delete(self):
        collection = GLDrawableCollection()
        collection.add(0, self.drawable)
        assert len(collection) == 1
        del collection[0]
        assert len(collection) == 0

    def test_items(self):
        collection = GLDrawableCollection()
        collection.add(0, self.drawable)
        drawable = collection[0]

        items = collection.items()
        assert list(items)[0][0] == 0
        assert list(items)[0][1] is drawable

    def test_clear(self):
        collection = GLDrawableCollection()
        collection.add(0, self.drawable)
        collection.add(1, self.drawable)
        collection.add(2, self.drawable)

        assert len(collection) == 3
        collection.clear()
        assert len(collection) == 0

    def test_draw(self):
        collection = GLDrawableCollection()
        drawable_1 = GLDrawable(widget=OpenGLWidget(), element=self.element)
        drawable_2 = GLDrawable(widget=OpenGLWidget(), element=self.element)
        collection.add(0, drawable_1)
        drawable_2.initialize()
        collection.add(1, drawable_2)
        collection.draw(None, None, None)
