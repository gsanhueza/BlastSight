#!/usr/bin/env python

import time


class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.fps = 0.0

    def tick(self):
        diff = time.time() - self.start_time
        self.fps = 1.0 / diff
        self.start_time = time.time()
