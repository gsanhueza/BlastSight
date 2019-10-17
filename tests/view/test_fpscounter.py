#!/usr/bin/env python

from blastsight.view.fpscounter import FPSCounter


class TestFPSCounter:
    def test_tick(self):
        counter = FPSCounter()
        assert counter.counter == 0
        assert counter.resolution == 1.0
        counter.tick()
        assert counter.counter == 1

    def test_resolution(self):
        counter = FPSCounter()
        counter.resolution = 0.0
        assert counter.counter == 0
        assert counter.resolution == 0.0

        counter.tick()

        assert counter.counter == 0
        assert counter.resolution == 0.0
