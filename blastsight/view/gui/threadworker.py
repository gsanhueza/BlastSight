#!/usr/bin/env python

from qtpy.QtCore import QRunnable


class ThreadWorker(QRunnable):
    def __init__(self, method, *args, **kwargs):
        super().__init__()
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.method(*self.args, **self.kwargs)
