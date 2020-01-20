#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.meshgl import MeshGL
from ..drawables.blockgl import BlockGL
from ..drawables.linegl import LineGL
from ..drawables.pointgl import PointGL
from ..drawables.tubegl import TubeGL

from ..glprograms.meshprogram import MeshProgram
from ..glprograms.wireprogram import WireProgram
from ..glprograms.blockprogram import BlockProgram
from ..glprograms.blocklegacyprogram import BlockLegacyProgram
from ..glprograms.lineprogram import LineProgram
from ..glprograms.pointprogram import PointProgram
from ..glprograms.tubeprogram import TubeProgram
from ..glprograms.turbomeshprogram import TurboMeshProgram


class GLDrawableCollection(GLCollection):
    def __init__(self, viewer=None):
        super().__init__(viewer)
        # Lines
        self.associate(LineProgram(viewer), lambda: self.filter(LineGL))

        # Tubes
        self.associate(TubeProgram(viewer), lambda: self.filter(TubeGL))

        # Points
        self.associate(PointProgram(viewer), lambda: self.filter(PointGL))

        # Blocks
        self.associate(BlockLegacyProgram(viewer), lambda: [
            x for x in self.filter(BlockGL) if x.is_legacy])

        self.associate(BlockProgram(viewer), lambda: [
            x for x in self.filter(BlockGL) if not x.is_legacy])

        # Meshes
        self.associate(TurboMeshProgram(viewer), lambda: [
            x for x in self.filter(MeshGL) if x.is_turbo_ready])
        self.associate(MeshProgram(viewer), lambda: [
            x for x in self.filter(MeshGL) if not x.is_turbo_ready and not x.is_wireframed])
        self.associate(WireProgram(viewer), lambda: [
            x for x in self.filter(MeshGL) if x.is_wireframed])
