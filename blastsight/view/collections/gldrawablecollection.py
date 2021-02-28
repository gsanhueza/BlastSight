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
from ..drawables.textgl import TextGL
from ..drawables.gridgl import GridGL

from ..glprograms.meshprogram import MeshProgram
from ..glprograms.wireprogram import WireProgram
from ..glprograms.highlightprogram import HighlightProgram
from ..glprograms.turbomeshprogram import TurboMeshProgram

from ..glprograms.blockprogram import BlockProgram
from ..glprograms.blocklegacyprogram import BlockLegacyProgram

from ..glprograms.lineprogram import LineProgram
from ..glprograms.pointprogram import PointProgram
from ..glprograms.tubeprogram import TubeProgram

from ..glprograms.meshphantomprogram import MeshPhantomProgram
from ..glprograms.xsectionmeshprogram import XSectionMeshProgram
from ..glprograms.xsectionblockprogram import XSectionBlockProgram

from ..glprograms.textprogram import TextProgram
from ..glprograms.gridprogram import GridProgram


class GLDrawableCollection(GLCollection):
    def generate_associations(self):
        # Lines/Tubes/Points
        self.associate(LineProgram(), LineGL)
        self.associate(TubeProgram(), TubeGL)
        self.associate(PointProgram(), PointGL)

        # Blocks
        self.associate(BlockLegacyProgram(), BlockGL, selector=lambda x: x.is_legacy)
        self.associate(BlockProgram(), BlockGL, selector=lambda x: x.is_standard)

        # Meshes
        self.associate(MeshProgram(), MeshGL, selector=lambda x: x.is_standard)
        self.associate(WireProgram(), MeshGL, selector=lambda x: x.is_wireframed)
        self.associate(HighlightProgram(), MeshGL, selector=lambda x: x.is_highlighted)
        self.associate(TurboMeshProgram(), MeshGL, selector=lambda x: x.is_turbo_ready)

        # XSection
        self.associate(MeshPhantomProgram(), MeshGL, selector=lambda x: x.is_phantom)
        self.associate(XSectionBlockProgram(), BlockGL, selector=lambda x: x.is_cross_sectionable)
        self.associate(XSectionMeshProgram(), MeshGL, selector=lambda x: x.is_cross_sectionable)

        # Text
        self.associate(TextProgram(), TextGL)

        # Axis
        self.associate(GridProgram(), GridGL)
