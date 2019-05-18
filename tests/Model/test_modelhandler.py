#!/usr/bin/env python

from Model.modelhandler import Singleton
from Model.modelhandler import model_handler
from Model.model import Model


class TestModelHandler:
    def test_original_instance(self):
        assert model_handler is not None

    def test_singleton(self):
        handler_1 = Singleton(Model)
        handler_2 = Singleton(Model)

        assert model_handler is handler_1
        assert handler_1 is handler_2
