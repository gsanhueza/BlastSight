#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import pathlib
from qtpy.QtGui import QIcon


class IconCollection:
    @staticmethod
    def get(path: str) -> QIcon:
        return QIcon(f'{pathlib.Path(__file__).parent}/UI/icons/{path}')
