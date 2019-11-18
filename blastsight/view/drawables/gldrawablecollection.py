#!/usr/bin/env python

#  Copyright (c) 2019 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from OpenGL.GL import *
from .glcollection import GLCollection

from .meshgl import MeshGL
from .blockgl import BlockGL
from .linegl import LineGL
from .pointgl import PointGL
from .tubegl import TubeGL

from .glprograms.meshprogram import MeshProgram
from .glprograms.wireprogram import WireProgram
from .glprograms.blockprogram import BlockProgram
from .glprograms.blocklegacyprogram import BlockLegacyProgram
from .glprograms.lineprogram import LineProgram
from .glprograms.pointprogram import PointProgram
from .glprograms.tubeprogram import TubeProgram
from .glprograms.turbomeshprogram import TurboMeshProgram


class GLDrawableCollection(GLCollection):
    def __init__(self, widget=None):
        super().__init__()
        # Lines
        self.programs[LineProgram(widget)] = lambda: self.filter(LineGL)

        # Tubes
        self.programs[TubeProgram(widget)] = lambda: self.filter(TubeGL)

        # Points
        self.programs[PointProgram(widget)] = lambda: self.filter(PointGL)

        # Blocks
        self.programs[BlockLegacyProgram(widget)] = lambda: [
            x for x in self.filter(BlockGL) if x.is_legacy]

        self.programs[BlockProgram(widget)] = lambda: [
            x for x in self.filter(BlockGL) if not x.is_legacy]

        # Meshes
        self.programs[TurboMeshProgram(widget)] = lambda: [
            x for x in self.filter(MeshGL) if x.is_turbo_ready]
        self.programs[MeshProgram(widget)] = lambda: [
            x for x in self.filter(MeshGL) if not x.is_turbo_ready and not x.is_wireframed]
        self.programs[WireProgram(widget)] = lambda: [
            x for x in self.filter(MeshGL) if x.is_wireframed]
