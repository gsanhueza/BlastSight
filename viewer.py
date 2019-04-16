#!/usr/bin/env python

from View.openglwidget import OpenGLWidget
from Model.model import Model


# Facade class (Extremely similar to MainWindow... but standalone)
class Viewer:
    def __init__(self, model=Model()):
        self.model = model
        self.opengl_viewer = OpenGLWidget(model=self.model)

        # Command queue
        self.queue = []
        self.mesh_ids = []

    def add_mesh(self, file_path: str):
        id_ = self.model.add_mesh(file_path)
        self.mesh_ids.append(id_)
        self.opengl_viewer.update_mesh()

    def update_mesh(self, id_: int, file_path: str):
        self.model.update_mesh(id_, file_path)

    def show_mesh(self, id_: int):
        self.opengl_viewer.show_mesh(id_)

    def hide_mesh(self, id_: int):
        self.opengl_viewer.hide_mesh(id_)

    def delete_mesh(self, id_: int):
        self.model.delete_mesh(id_)

    def add_block_model(self, file_path: str):
        self.model.add_block_model(file_path)
        self.opengl_viewer.update_block_model()

    def delete_block_model(self):
        pass

    def toggle_mesh_wireframe(self, id_: int):
        self.queue.append(lambda: self.opengl_viewer.toggle_wireframe())

    def set_camera_position(self, x: float, y: float, z: float):
        self.opengl_viewer.set_camera_pos(x, y, z)

    def show(self):
        self.opengl_viewer.show()

        # Execute queued commands needed *after* opengl shows itself
        for command in self.queue:
            command()


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    from Model.model import Model

    qt_app = QApplication()
    model = Model()

    model.add_mesh('Model/Mesh/caseron.off')
    model.add_block_model('Model/BlockModel/mini.csv')

    viewer = Viewer(model)
    viewer.show()

    sys.exit(qt_app.exec_())
