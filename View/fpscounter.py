#!/usr/bin/env python

import time


class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.seconds_resolution = 1
        self.counter = 0

    def __str__(self):
        return f'FPS: {self.counter / (time.time() - self.start_time)}'  # FPS = 1 / time to process loop

    def tick(self):
        self.counter += 1
        if (time.time() - self.start_time) > self.seconds_resolution:
            print(self)
            self.counter = 0
            self.start_time = time.time()
