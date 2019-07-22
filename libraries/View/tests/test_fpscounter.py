#!/usr/bin/env python

from libraries.View.fpscounter import FPSCounter


class TestFPSCounter:
    def test_fps_counter(self):
        counter = FPSCounter()

        assert counter.seconds_resolution == 1
        assert counter.counter == 0

    def test_tick(self):
        counter = FPSCounter()
        counter.tick()

        assert counter.seconds_resolution == 1
        assert counter.counter == 1

        counter.tick()
        assert counter.seconds_resolution == 1
        assert counter.counter == 2

    def test_print(self):
        counter = FPSCounter()
        assert counter.__str__() == 'FPS: 0.0'

    def test_resolution(self):
        counter = FPSCounter()
        counter.seconds_resolution = 0
        assert counter.__str__() == 'FPS: 0.0'

        counter.tick()
        assert counter.__str__() == 'FPS: 0.0'
