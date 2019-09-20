#!/usr/bin/env python

from .element import Element


class NullElement(Element):
    def __init__(self, *args, **kwargs):
        """
        NullElement is a placeholder for AxisGL and BackgroundGL.
        It has no data associated.
        """
        super().__init__(*args, **kwargs)

    def _fill_element(self, *args, **kwargs):
        pass

    def _check_integrity(self):
        pass
