#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import time


class FPSCounter:
    def __init__(self, resolution: float = 1.0):
        self.start_time = time.time()
        self.resolution = resolution
        self.counter = 0

    def tick(self, callback=lambda *args: None) -> None:
        self.counter += 1
        if time.time() - self.start_time > self.resolution:
            diff = (time.time() - self.start_time)
            callback(self.counter / diff if diff else 0.0)
            self.counter = 0
            self.start_time = time.time()
