#!/usr/bin/env python

import pytest
from blastsight.model.parsers.parser import Parser
from blastsight.model.parsers.offparser import OFFParser
from blastsight.model.parsers.parsercollection import ParserCollection


class TestParser:
    def test_load(self):
        with pytest.raises(NotImplementedError):
            Parser.load_file('')

    def test_save(self):
        with pytest.raises(NotImplementedError):
            Parser.save_file('')

    def test_collection(self):
        collection = ParserCollection()
        collection.add('off', OFFParser())
        assert len(collection._collection) == 1
        assert isinstance(collection.get('off'), OFFParser)

        with pytest.raises(KeyError):
            collection.delete('aaa')
        assert len(collection._collection) == 1

        collection.delete('off')
        assert len(collection._collection) == 0
