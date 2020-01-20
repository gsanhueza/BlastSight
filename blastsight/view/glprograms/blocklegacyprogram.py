#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .shaderprogram import ShaderProgram


class BlockLegacyProgram(ShaderProgram):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.base_name = 'BlockLegacy'
