#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import QRunnable


class ThreadWorker(QRunnable):
    def __init__(self, method, *args, **kwargs):
        super().__init__()
        self.method = method
        self.callback = kwargs.pop('callback', lambda *a, **k: None)
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        self.callback(self.method(*self.args, **self.kwargs))
