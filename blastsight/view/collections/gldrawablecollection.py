#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from .glcollection import GLCollection

from ..drawables.meshgl import MeshGL
from ..drawables.blockgl import BlockGL
from ..drawables.linegl import LineGL
from ..drawables.pointgl import PointGL
from ..drawables.textgl import TextGL
from ..drawables.tubegl import TubeGL

from ..drawables.blocklegacygl import BlockLegacyGL
from ..drawables.tubelegacygl import TubeLegacyGL

from ..glprograms.meshprogram import MeshProgram
from ..glprograms.wireprogram import WireProgram
from ..glprograms.highlightprogram import HighlightProgram
from ..glprograms.turbomeshprogram import TurboMeshProgram

from ..glprograms.blockprogram import BlockProgram
from ..glprograms.blocklegacyprogram import BlockLegacyProgram

from ..glprograms.lineprogram import LineProgram
from ..glprograms.pointprogram import PointProgram
from ..glprograms.tubeprogram import TubeProgram
from ..glprograms.tubelegacyprogram import TubeLegacyProgram

from ..glprograms.meshphantomprogram import MeshPhantomProgram
from ..glprograms.xsectionmeshprogram import XSectionMeshProgram
from ..glprograms.xsectionblockprogram import XSectionBlockProgram

from ..glprograms.textprogram import TextProgram


class GLDrawableCollection(GLCollection):
    def generate_associations(self):
        # Lines/Points
        self.associate(LineProgram(), LineGL)
        self.associate(PointProgram(), PointGL)

        # Tubes
        self.associate(TubeLegacyProgram(), TubeLegacyGL)
        self.associate(TubeProgram(), TubeGL)

        # Blocks
        self.associate(BlockLegacyProgram(), BlockLegacyGL, selector=lambda x: x.is_standard)
        self.associate(BlockProgram(), BlockGL, selector=lambda x: x.is_standard)

        # Meshes
        self.associate(MeshProgram(), MeshGL, selector=lambda x: x.is_standard)
        self.associate(WireProgram(), MeshGL, selector=lambda x: x.is_wireframed)
        self.associate(HighlightProgram(), MeshGL, selector=lambda x: x.is_highlighted)
        self.associate(TurboMeshProgram(), MeshGL, selector=lambda x: x.is_turbo_ready)

        # XSection
        self.associate(MeshPhantomProgram(), MeshGL, selector=lambda x: x.is_phantom)
        self.associate(XSectionBlockProgram(), BlockGL, selector=lambda x: x.is_cross_sectioned)
        self.associate(XSectionMeshProgram(), MeshGL, selector=lambda x: x.is_cross_sectioned)

        # Text
        self.associate(TextProgram(), TextGL)
