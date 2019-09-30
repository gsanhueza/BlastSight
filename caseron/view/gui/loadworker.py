#!/usr/bin/env python

from qtpy.QtCore import QRunnable


class LoadWorker(QRunnable):
    def __init__(self, method, path):
        super().__init__()
        self.method = method
        self.path = path

    def run(self):
        self.method(self.path)
