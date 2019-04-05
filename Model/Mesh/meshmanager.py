#!/usr/bin/env python

from Model.handler import Handler
from Model.Mesh.dxfhandler import DXFHandler
from Model.Mesh.offhandler import OFFHandler
from Model.BlockModel.csvhandler import CSVHandler


# Generic handler for mesh loading/saving
class MeshManager:
    def __init__(self):
        self.handler_dict = {}
        self.add_handler('dxf', DXFHandler())
        self.add_handler('off', OFFHandler())
        self.add_handler('csv', CSVHandler())

    # Adds a new handler for meshes
    def add_handler(self, extension: str, handler: Handler) -> None:
        self.handler_dict[extension] = handler

    # Returns the handler that matches the current extension
    def get_handler(self, ext: str) -> Handler:
        # Example: {"dxf": DXFHandler, "off": OFFHandler}
        return self.handler_dict[ext]

    # Lets the handler load the mesh and update the model
    def load_mesh(self, model, file_path: str) -> bool:
        ext = Handler.get_file_extension(file_path)
        return self.get_handler(ext).load_mesh(model, file_path)

    # Lets the handler save the mesh
    def save_mesh(self, model, file_path: str) -> bool:
        ext = Handler.get_file_extension(file_path)
        return self.get_handler(ext).save_mesh(model, file_path)
