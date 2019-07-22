#!/usr/bin/env python

import time


class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.seconds_resolution = 1
        self.counter = 0

    def __str__(self):
        diff = (time.time() - self.start_time)

        # FPS = 1 / time to process loop
        return f'FPS: {self.counter / diff}' if diff else f'FPS: 0.0'

    def tick(self):
        self.counter += 1
        if (time.time() - self.start_time) > self.seconds_resolution:
            print(f'{self.__str__()}\r', end='')
            self.counter = 0
            self.start_time = time.time()
