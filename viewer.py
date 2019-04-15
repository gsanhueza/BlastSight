#!/usr/bin/env python

from View.openglwidget import OpenGLWidget
from PySide2.QtWidgets import QWidget


# Facade class (Extremely similar to MainWindow... but standalone)
class Viewer:
    def __init__(self, model=None):
        self.model = model
        self.opengl_viewer = OpenGLWidget(model=model)

        # Command queue
        self.queue = []
        self.mesh_ids = []

    def add_mesh(self, file_path: str):
        _id = self.model.add_mesh(file_path)
        self.mesh_ids.append(_id)
        self.opengl_viewer.update_mesh()

    def update_mesh(self, _id: int):
        self.model.update_mesh(_id)

    def hide_mesh(self, _id: int):
        pass

    def delete_mesh(self, _id: int):
        self.model.delete_mesh(_id)

    def add_block_model(self, file_path: str):
        self.model.add_block_model(file_path)

    def delete_block_model(self):
        pass

    def toggle_mesh_wireframe(self, _id: int):
        pass

    def set_camera_position(self, x: float, y: float, z: float):
        self.opengl_viewer.set_camera_pos(x, y, z)

    def show(self):
        self.opengl_viewer.show()


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    from Model.model import Model

    qt_app = QApplication()
    model = Model()
    viewer = Viewer(model)
    viewer.set_camera_position(0, 0, -20)
    viewer.add_mesh('Model/Mesh/caseron.off')

    viewer.show()

    sys.exit(qt_app.exec_())
