#!/usr/bin/env python

from Model.handler import Handler
from Model.BlockModel.csvparser import CSVParser


# OFF handler for mesh loading/saving
class CSVHandler(Handler):
    def __init__(self):
        self.parser = CSVParser()
