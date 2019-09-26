#!/usr/bin/env python

from qtpy.QtCore import QRunnable, Signal, QObject


class WorkerSignals(QObject):
    loaded = Signal(int)


class LoadWorker(QRunnable):

    def __init__(self, method, path):
        super().__init__()
        self.method = method
        self.path = path
        self.signals = WorkerSignals()

    def run(self):
        drawable = self.method(self.path)
        if drawable:
            self.signals.loaded.emit(drawable.id)
