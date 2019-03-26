#/usr/bin/env python

from .csvhandler import CSVHandler


# Generic handler for block model loading
# Receives a reference to the model and a default handler
class BlockModelHandler:
    def __init__(self):
        self.handler_dict = {}
        self.current_extension = 'csv'
        self.add_handler(self.current_extension, CSVHandler())

    def add_handler(self, extension, handler):
        self.handler_dict[extension] = handler

    def get_handler(self):
        # FIXME If we have more than just a CSV handler, we might want to update this to use a dictionary with the extension as a key
        # {"csv": CSVHandler, "xls": ExcelHandler}, for example.
        return self.handler_dict[current_extension]

    # Lets the handler load the block model and update the internal model
    def load_blockmodel(self, model, filepath):
        self.get_handler().load_blockmodel(model, filepath)

    # Lets the handler save the block model by reading the internal model
    def save_blockmodel(self, model, filepath):
        self.get_handler().save_blockmodel(model, filepath)
