#!/usr/bin/env python

from qtpy.QtCore import QRunnable


class ThreadWorker(QRunnable):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    def run(self):
        method = self.kwargs.pop('method')
        method(*self.args, **self.kwargs)
