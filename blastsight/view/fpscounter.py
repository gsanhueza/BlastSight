#!/usr/bin/env python

#  Copyright (c) 2019-2021 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import time


class FPSCounter:
    def __init__(self, resolution: float = 1.0):
        self.start_time = time.time()
        self.resolution = resolution
        self.callbacks = []
        self.counter = 0

    def add_callback(self, callback: callable) -> None:
        self.callbacks.append(callback)

    def pop_callback(self) -> callable:
        return self.callbacks.pop()

    def clear_callbacks(self) -> None:
        self.callbacks.clear()

    def notify(self, fps: float) -> None:
        for callback in self.callbacks:
            callback(fps)

    def tick(self) -> None:
        self.counter += 1
        if time.time() - self.start_time > self.resolution:
            diff = (time.time() - self.start_time)
            self.notify(self.counter / diff if diff else 0.0)

            self.counter = 0
            self.start_time = time.time()
