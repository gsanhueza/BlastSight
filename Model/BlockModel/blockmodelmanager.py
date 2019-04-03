#!/usr/bin/env python

from Model.handler import Handler
from Model.BlockModel.csvhandler import CSVHandler


# Generic handler for block model loading/saving
class BlockModelManager:
    def __init__(self):
        self.handler_dict = {}
        self.add_handler('csv', CSVHandler())

    # Adds a new handler for block models
    def add_handler(self, extension: str, handler: Handler) -> None:
        self.handler_dict[extension] = handler

    # Returns the handler that matches the current extension
    def get_handler(self, ext: str) -> Handler:
        # Example: {"csv": CSVHandler, "xls": ExcelHandler}
        return self.handler_dict[ext]

    # Lets the handler load the block model and update the model
    def load_blockmodel(self, model, file_path: str) -> bool:
        ext = Handler.get_file_extension(file_path)
        return self.get_handler(ext).load_mesh(model, file_path)

    # Lets the handler save the block model
    def save_blockmodel(self, model, file_path: str) -> bool:
        ext = Handler.get_file_extension(file_path)
        return self.get_handler(ext).save_mesh(model, file_path)
