#!/usr/bin/env python

import time


class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.fps = 0.0
        self.resolution = 1.0
        self.counter = 0

    def tick(self):
        self.counter += 1
        if time.time() - self.start_time > self.resolution:
            diff = (time.time() - self.start_time)

            self.fps = self.counter / diff if diff else 0.0
            self.counter = 0
            self.start_time = time.time()
