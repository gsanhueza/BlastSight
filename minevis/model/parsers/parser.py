#!/usr/bin/env python

from .parserdata import ParserData

"""
Pandas' current version (0.25) has an ugly memory leak when reading files (tested empirically).
Since MineVis is not meant to improve Pandas, we'll implement a workaround from
https://github.com/pandas-dev/pandas/issues/2659#issuecomment-415177442

"""
import sys
import pandas as pd
from ctypes import cdll, CDLL
try:
    cdll.LoadLibrary("libc.so.6")
    libc = CDLL("libc.so.6")
    libc.malloc_trim(0)
except (OSError, AttributeError):
    libc = None

__old_del = getattr(pd.DataFrame, '__del__', None)


def __new_del(self):
    if __old_del:
        __old_del(self)
    libc.malloc_trim(0)


if libc:
    print('Applying monkeypatch for pd.DataFrame.__del__', file=sys.stderr)
    pd.DataFrame.__del__ = __new_del
else:
    print('Skipping monkeypatch for pd.DataFrame.__del__: libc or malloc_trim() not found', file=sys.stderr)


class Parser:
    @staticmethod
    def load_file(path: str) -> ParserData:
        raise NotImplementedError

    @staticmethod
    def save_file(path: str, *args, **kwargs) -> None:
        raise NotImplementedError
