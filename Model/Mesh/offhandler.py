#!/usr/bin/env python

from Model.handler import Handler
from Model.Mesh.offparser import OFFParser


# OFF handler for mesh loading/saving
# The loading is deferred to the parser
# We need to know how to save it now...
class OFFHandler(Handler):
    def __init__(self):
        self.parser = OFFParser()

