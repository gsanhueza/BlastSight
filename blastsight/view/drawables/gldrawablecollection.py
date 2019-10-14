#!/usr/bin/env python

from .glcollection import GLCollection

from .meshgl import MeshGL
from .blockgl import BlockGL
from .linegl import LineGL
from .pointgl import PointGL
from .tubegl import TubeGL

from .glprograms.meshprogram import MeshProgram
from .glprograms.wireprogram import WireProgram
from .glprograms.blockprogram import BlockProgram
from .glprograms.lineprogram import LineProgram
from .glprograms.pointprogram import PointProgram
from .glprograms.tubeprogram import TubeProgram
from .glprograms.batchmeshprogram import BatchMeshProgram


class GLDrawableCollection(GLCollection):
    def __init__(self, widget=None):
        super().__init__()
        self.programs[BlockProgram(widget)] = lambda: self.filter(BlockGL)
        self.programs[LineProgram(widget)] = lambda: self.filter(LineGL)
        self.programs[TubeProgram(widget)] = lambda: self.filter(TubeGL)
        self.programs[PointProgram(widget)] = lambda: self.filter(PointGL)
        self.programs[BatchMeshProgram(widget)] = lambda: [
            x for x in self.filter(MeshGL) if x.is_batchable]
        self.programs[MeshProgram(widget)] = lambda: [
            x for x in self.filter(MeshGL) if not x.is_batchable and not x.is_wireframed]
        self.programs[WireProgram(widget)] = lambda: [
            x for x in self.filter(MeshGL) if not x.is_batchable and x.is_wireframed]
