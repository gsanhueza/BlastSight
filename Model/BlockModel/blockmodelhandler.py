#/usr/bin/env python

from .csvhandler import CSVHandler


# Generic handler for block model loading
# Receives a reference to the model and a default handler
class BlockModelHandler:
    def __init__(self):
        self.handler_dict = {}
        self.current_extension = 'csv'
        self.add_handler(self.current_extension, CSVHandler())

    # Adds a new handler for meshes
    def add_handler(self, extension, handler):
        self.handler_dict[extension] = handler

    # Returns the handler that matches the current extension
    def get_handler(self):
        # FIXME If we have more than just a CSV handler, we might want to update this to use a dictionary with the extension as a key
        # {"csv": CSVHandler, "xls": ExcelHandler}, for example.
        return self.handler_dict[self.current_extension]

    # Lets the handler load the block model and update the internal model
    # Returns a boolean
    def load_blockmodel(self, model, filepath):
        self.get_handler().load_blockmodel(model, filepath)

    # Lets the handler save the block model by reading the internal model
    # Returns a boolean
    def save_blockmodel(self, model, filepath):
        self.get_handler().save_blockmodel(model, filepath)
