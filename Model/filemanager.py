#!/usr/bin/env python

from Model.Mesh.meshhandler import MeshHandler
from Model.BlockModel.blockmodelhandler import BlockModelHandler


class FileManager:
    def __init__(self):
        self.mesh_handler = MeshHandler()
        self.block_model_handler = BlockModelHandler()

    def load_mesh(self, model, file_path: str) -> bool:
        return self.mesh_handler.load(model, file_path)

    def save_mesh(self, model, file_path: str) -> bool:
        return self.mesh_handler.save(model, file_path)

    def load_block_model(self, model, file_path: str) -> bool:
        return self.block_model_handler.load(model, file_path)

    def save_block_model(self, model, file_path: str) -> bool:
        return self.block_model_handler.save(model, file_path)
