#!/usr/bin/env python

from qtpy.QtCore import QRunnable


class ExportWorker(QRunnable):
    def __init__(self, method: classmethod, path: str, _id: int):
        super().__init__()
        self.method = method
        self.path = path
        self.id = _id

    def run(self):
        self.method(self.path, self.id)
