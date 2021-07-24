#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .element import Element


class NullElement(Element):
    def __init__(self, *args, **kwargs):
        """
        NullElement is a placeholder for AxisGL and BackgroundGL.
        It has no data associated.
        """
        super().__init__(*args, **kwargs)

    def _fill_element(self, *args, **kwargs) -> None:
        pass

    def _check_integrity(self) -> None:
        pass
