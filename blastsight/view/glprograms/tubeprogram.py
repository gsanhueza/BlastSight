#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram


class TubeProgram(ShaderProgram):
    def __init__(self):
        super().__init__()
        self.base_name = 'Tube'
