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
        # Lines/Tubes/Points
        self.associate(LineProgram(viewer), LineGL)
        self.associate(TubeProgram(viewer), TubeGL)
        self.associate(PointProgram(viewer), PointGL)

        # Blocks
        self.associate(BlockLegacyProgram(viewer), BlockGL, selector=lambda x: x.is_legacy)
        self.associate(BlockProgram(viewer), BlockGL, selector=lambda x: x.is_standard)

        # Meshes
        self.associate(MeshProgram(viewer), MeshGL, selector=lambda x: x.is_standard)
        self.associate(WireProgram(viewer), MeshGL, selector=lambda x: x.is_wireframed)
        self.associate(HighlightProgram(viewer), MeshGL, selector=lambda x: x.is_highlighted)
        self.associate(TurboMeshProgram(viewer), MeshGL, selector=lambda x: x.is_turbo_ready)
        self.associate(CrossSectionProgram(viewer), MeshGL, selector=lambda x: x.is_cross_sectionable)
