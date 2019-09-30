#!/usr/bin/env python

from qtpy.QtCore import QRunnable, Signal, QObject


class WorkerSignals(QObject):
    success = Signal(int)
    failure = Signal()


class LoadWorker(QRunnable):
    def __init__(self, method, path):
        super().__init__()
        self.method = method
        self.path = path
        self.signals = WorkerSignals()

    def run(self):
        drawable = self.method(self.path)
        if drawable:
            self.signals.success.emit(drawable.id)
        else:
            self.signals.failure.emit()
