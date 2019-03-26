#/usr/bin/env python

from .dxfhandler import DXFHandler


# Generic handler for mesh loading
# Receives a reference to the model and a default handler
class MeshHandler:
    def __init__(self):
        self.handler_dict = {}
        self.current_extension = 'dxf'
        self.add_handler(self.current_extension, DXFHandler())

    # Adds a new handler for meshes
    def add_handler(self, extension: str, handler) -> None:
        self.handler_dict[extension] = handler

    # Returns the handler that matches the current extension
    def get_handler(self):
        # FIXME If we have more than just a DXF handler, we might want to update this to use a dictionary with the extension as a key
        # {"dxf": DXFHandler, "off": OFFHandler}, for example.
        return self.handler_dict[self.current_extension]

    # Lets the handler load the mesh and update the model
    # Returns a boolean
    def load_mesh(self, model, filepath: str) -> bool:
        return self.get_handler().load_mesh(model, filepath)

    # Lets the handler save the mesh and update the model
    # Returns a boolean
    def save_mesh(self, model, filepath: str) -> bool:
        return self.get_handler().save_mesh(model, filepath)
