#!/usr/bin/env python

from libraries.View.fpscounter import FPSCounter


class TestFPSCounter:
    def test_tick(self):
        counter = FPSCounter()
        assert counter.fps == 0.0
        counter.tick()
        assert counter.fps > 0.0
