#!/usr/bin/env python

from .glcollection import GLCollection

from .meshgl import MeshGL
from .blockgl import BlockGL
from .linegl import LineGL
from .pointgl import PointGL
from .tubegl import TubeGL

from .glprograms.meshprogram import MeshProgram
from .glprograms.blockprogram import BlockProgram
from .glprograms.lineprogram import LineProgram
from .glprograms.pointprogram import PointProgram
from .glprograms.tubeprogram import TubeProgram


class GLDrawableCollection(GLCollection):
    def __init__(self, widget=None):
        super().__init__()
        self.programs[BlockProgram(widget)] = lambda: self.filter(BlockGL)
        self.programs[LineProgram(widget)] = lambda: self.filter(LineGL)
        self.programs[TubeProgram(widget)] = lambda: self.filter(TubeGL)
        self.programs[PointProgram(widget)] = lambda: self.filter(PointGL)
        self.programs[MeshProgram(widget)] = lambda: self.filter(MeshGL)
