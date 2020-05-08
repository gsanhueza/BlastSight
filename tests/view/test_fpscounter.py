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

    def test_callbacks(self):
        counter = FPSCounter()
        test_list = []

        def my_callback(x):
            test_list.append(x)

        def my_callback2(x):
            test_list.append(2 * x)

        counter.add_callback(my_callback)
        assert len(counter.callbacks) == 1
        assert len(test_list) == 0

        counter.notify(1)
        assert len(test_list) == 1
        assert test_list[0] == 1

        counter.add_callback(my_callback2)
        assert len(counter.callbacks) == 2
        assert len(test_list) == 1

        counter.notify(5)
        assert len(test_list) == 3
        assert test_list[0] == 1
        assert test_list[1] == 5
        assert test_list[2] == 10

        counter.pop_callback()
        assert len(counter.callbacks) == 1
        assert len(test_list) == 3

        counter.add_callback(my_callback)
        counter.add_callback(my_callback)
        counter.add_callback(my_callback)

        assert len(counter.callbacks) == 4

        counter.clear_callbacks()
        assert len(counter.callbacks) == 0
