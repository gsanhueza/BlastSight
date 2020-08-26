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
from ..glprograms.highlightprogram import HighlightProgram
from ..glprograms.turbomeshprogram import TurboMeshProgram
from ..glprograms.crosssectionprogram import CrossSectionProgram

from ..glprograms.blockprogram import BlockProgram
from ..glprograms.blocklegacyprogram import BlockLegacyProgram

from ..glprograms.lineprogram import LineProgram
from ..glprograms.pointprogram import PointProgram
from ..glprograms.tubeprogram import TubeProgram


class GLDrawableCollection(GLCollection):
    def __init__(self, viewer=None):
        super().__init__(viewer)
        self.associate(LineProgram(viewer), lambda: self.select(LineGL))
        self.associate(TubeProgram(viewer), lambda: self.select(TubeGL))
        self.associate(PointProgram(viewer), lambda: self.select(PointGL))

        # Blocks
        self.associate(BlockLegacyProgram(viewer), lambda: self.select(BlockGL, 'block_legacy'))
        self.associate(BlockProgram(viewer), lambda: self.select(BlockGL, 'block_standard'))

        # Meshes
        self.associate(MeshProgram(viewer), lambda: self.select(MeshGL, 'mesh_standard'))
        self.associate(WireProgram(viewer), lambda: self.select(MeshGL, 'mesh_wireframe'))
        self.associate(HighlightProgram(viewer), lambda: self.select(MeshGL, 'mesh_highlight'))
        self.associate(TurboMeshProgram(viewer), lambda: self.select(MeshGL, 'mesh_turbo'))
        self.associate(CrossSectionProgram(viewer), lambda: self.select(MeshGL, 'mesh_xsection'))
