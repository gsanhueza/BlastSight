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
        self.associate(LineProgram(viewer), lambda: self.retrieve(LineGL))
        self.associate(TubeProgram(viewer), lambda: self.retrieve(TubeGL))
        self.associate(PointProgram(viewer), lambda: self.retrieve(PointGL))

        # Blocks
        self.associate(BlockLegacyProgram(viewer), lambda: self.retrieve(BlockGL, 'block_legacy'))
        self.associate(BlockProgram(viewer), lambda: self.retrieve(BlockGL, 'block_standard'))

        # Meshes
        self.associate(TurboMeshProgram(viewer), lambda: self.retrieve(MeshGL, 'mesh_turbo'))
        self.associate(MeshProgram(viewer), lambda: self.retrieve(MeshGL, 'mesh_standard'))
        self.associate(WireProgram(viewer), lambda: self.retrieve(MeshGL, 'mesh_wireframe'))
